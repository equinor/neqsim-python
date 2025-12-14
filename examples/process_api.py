"""
NeqSim Process Simulation API

A REST API for running process simulations from YAML/JSON configurations.

Usage:
    1. Install dependencies:
       pip install fastapi uvicorn pyyaml

    2. Run the API server:
       uvicorn process_api:app --reload --port 8000

    3. Open API docs:
       http://localhost:8000/docs

    4. Send POST request with process configuration:
       curl -X POST http://localhost:8000/simulate \\
            -H "Content-Type: application/json" \\
            -d @process_config.json

Example request body (JSON):
{
    "name": "Simple Compression",
    "fluids": {
        "feed": {
            "model": "srk",
            "temperature": 303.15,
            "pressure": 10.0,
            "components": [
                {"name": "methane", "moles": 0.9},
                {"name": "ethane", "moles": 0.1}
            ]
        }
    },
    "equipment": [
        {"type": "stream", "name": "inlet", "fluid": "feed",
         "flow_rate": 5.0, "flow_unit": "MSm3/day"},
        {"type": "compressor", "name": "comp1", "inlet": "inlet",
         "pressure": 50.0}
    ]
}
"""

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional, Union
import json
import traceback

# Initialize NeqSim (must be done before importing process modules)
try:
    from neqsim.process import create_process_from_config, create_fluid_from_config
    from neqsim.thermo import TPflash, dataFrame
    NEQSIM_AVAILABLE = True
except ImportError as e:
    NEQSIM_AVAILABLE = False
    NEQSIM_ERROR = str(e)

# FastAPI app
app = FastAPI(
    title="NeqSim Process Simulation API",
    description="REST API for running process simulations from YAML/JSON configurations",
    version="1.0.0",
)

# Enable CORS for web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# Pydantic Models for Request/Response
# =============================================================================


class ComponentConfig(BaseModel):
    """Component configuration for fluid creation."""
    name: str = Field(..., description="Component name (e.g., 'methane', 'CO2')")
    moles: Optional[float] = Field(None, description="Molar amount")
    rate: Optional[float] = Field(None, description="Flow rate")
    unit: Optional[str] = Field("mol/sec", description="Flow rate unit")
    mole_fraction: Optional[float] = Field(None, description="Mole fraction")


class FluidConfig(BaseModel):
    """Fluid configuration."""
    type: Optional[str] = Field("custom", description="'predefined' or 'custom'")
    name: Optional[str] = Field(None, description="Predefined fluid name")
    model: Optional[str] = Field("srk", description="Equation of state")
    temperature: Optional[float] = Field(298.15, description="Temperature in K")
    pressure: Optional[float] = Field(1.01325, description="Pressure in bara")
    components: Optional[List[ComponentConfig]] = Field(None, description="Component list")
    mixing_rule: Optional[str] = Field(None, description="Mixing rule")
    ge_model: Optional[str] = Field(None, description="GE model")
    multiphase: Optional[bool] = Field(False, description="Enable multiphase")
    solid_check: Optional[bool] = Field(False, description="Enable solid check")


class EquipmentConfig(BaseModel):
    """Equipment configuration."""
    type: str = Field(..., description="Equipment type (e.g., 'stream', 'compressor')")
    name: str = Field(..., description="Unique equipment name")
    
    class Config:
        extra = "allow"  # Allow additional fields for equipment-specific params


class ProcessConfig(BaseModel):
    """Complete process configuration."""
    name: Optional[str] = Field("Process", description="Process name")
    fluids: Optional[Dict[str, FluidConfig]] = Field(None, description="Fluid definitions")
    equipment: List[EquipmentConfig] = Field(..., description="Equipment list")


class FlashRequest(BaseModel):
    """Request for flash calculation."""
    fluid: FluidConfig = Field(..., description="Fluid configuration")
    temperature: Optional[float] = Field(None, description="Flash temperature in K")
    pressure: Optional[float] = Field(None, description="Flash pressure in bara")


class SimulationResult(BaseModel):
    """Simulation result response."""
    success: bool
    process_name: str
    equipment_results: Dict[str, Any]
    stream_data: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None


class FlashResult(BaseModel):
    """Flash calculation result."""
    success: bool
    temperature: float
    pressure: float
    phases: List[Dict[str, Any]]
    properties: Dict[str, Any]
    error: Optional[str] = None


# =============================================================================
# API Endpoints
# =============================================================================


@app.get("/")
async def root():
    """API health check and info."""
    return {
        "service": "NeqSim Process Simulation API",
        "version": "1.0.0",
        "neqsim_available": NEQSIM_AVAILABLE,
        "docs_url": "/docs",
        "endpoints": {
            "POST /simulate": "Run process simulation from config",
            "POST /flash": "Run flash calculation",
            "GET /equipment-types": "List available equipment types",
            "GET /fluid-models": "List available equation of state models",
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    if not NEQSIM_AVAILABLE:
        raise HTTPException(status_code=503, detail=f"NeqSim not available: {NEQSIM_ERROR}")
    return {"status": "healthy", "neqsim": "available"}


@app.get("/equipment-types")
async def get_equipment_types():
    """Get list of available equipment types for YAML/JSON configuration."""
    equipment_types = {
        "streams": [
            "stream", "water_stream", "neq_stream", "energy_stream",
            "well_stream", "virtual_stream", "stream_from_outlet"
        ],
        "separators": [
            "separator", "three_phase_separator", "gas_scrubber",
            "gas_scrubber_with_options", "separator_with_dimensions"
        ],
        "pressure_changers": [
            "compressor", "pump", "expander", "valve", "valve_with_options",
            "compressor_with_chart", "polytopic_compressor", "polytropic_compressor"
        ],
        "heat_transfer": [
            "heater", "cooler", "heat_exchanger"
        ],
        "mixing_splitting": [
            "mixer", "splitter", "manifold", "static_mixer",
            "static_phase_mixer", "component_splitter", "splitter_with_flowrates"
        ],
        "pipelines": [
            "pipe", "beggs_brill_pipe", "two_phase_pipe"
        ],
        "columns": [
            "distillation_column", "teg_absorber", "water_stripper", "simple_absorber"
        ],
        "reactors": [
            "reactor", "gibbs_reactor"
        ],
        "utilities": [
            "saturator", "filter", "calculator", "setpoint",
            "adjuster", "ejector", "flare", "tank"
        ],
        "measurement": [
            "pressure_transmitter", "level_transmitter",
            "flow_transmitter", "temperature_transmitter"
        ],
        "control": [
            "pid_controller", "flow_setter", "flow_rate_adjuster"
        ],
        "recycle": [
            "recycle", "recycle_loop", "close_recycle"
        ]
    }
    return equipment_types


@app.get("/fluid-models")
async def get_fluid_models():
    """Get list of available equation of state models."""
    return {
        "cubic_eos": [
            {"id": "srk", "name": "Soave-Redlich-Kwong"},
            {"id": "pr", "name": "Peng-Robinson"},
            {"id": "rk", "name": "Redlich-Kwong"},
        ],
        "advanced_eos": [
            {"id": "cpa", "name": "CPA (Cubic Plus Association)"},
            {"id": "cpa-srk", "name": "CPA-SRK"},
            {"id": "cpa-pr", "name": "CPA-PR"},
            {"id": "gerg-2008", "name": "GERG-2008"},
        ],
        "electrolyte": [
            {"id": "electrolyte", "name": "Electrolyte EoS"},
            {"id": "cpa-el", "name": "Electrolyte CPA"},
        ],
        "activity_coefficient": [
            {"id": "nrtl", "name": "NRTL"},
            {"id": "unifac", "name": "UNIFAC"},
        ],
        "predefined_fluids": [
            "dry gas", "rich gas", "light oil", "black oil",
            "water", "air", "combustion air"
        ]
    }


@app.post("/simulate", response_model=SimulationResult)
async def run_simulation(
    config: ProcessConfig = Body(..., example={
        "name": "Simple Compression",
        "fluids": {
            "feed": {
                "model": "srk",
                "temperature": 303.15,
                "pressure": 10.0,
                "components": [
                    {"name": "methane", "moles": 0.9},
                    {"name": "ethane", "moles": 0.1}
                ]
            }
        },
        "equipment": [
            {"type": "stream", "name": "inlet", "fluid": "feed",
             "flow_rate": 5.0, "flow_unit": "MSm3/day"},
            {"type": "compressor", "name": "comp1", "inlet": "inlet",
             "pressure": 50.0}
        ]
    })
):
    """
    Run a process simulation from JSON configuration.
    
    The configuration should include:
    - name: Optional process name
    - fluids: Dictionary of fluid configurations
    - equipment: List of equipment in process order
    
    Returns simulation results including equipment data and stream properties.
    """
    if not NEQSIM_AVAILABLE:
        raise HTTPException(status_code=503, detail=f"NeqSim not available: {NEQSIM_ERROR}")
    
    try:
        # Convert Pydantic model to dict
        config_dict = config.model_dump(exclude_none=True)
        
        # Convert fluids config
        if "fluids" in config_dict:
            fluids_dict = {}
            for name, fluid_cfg in config_dict["fluids"].items():
                fluids_dict[name] = fluid_cfg
            config_dict["fluids"] = fluids_dict
        
        # Run simulation
        process = create_process_from_config(config_dict, run=True)
        
        # Collect results
        equipment_results = {}
        for eq_name, eq_obj in process.equipment.items():
            eq_result = {"name": eq_name, "type": type(eq_obj).__name__}
            
            # Try to get common properties
            try:
                if hasattr(eq_obj, "getOutletStream"):
                    outlet = eq_obj.getOutletStream()
                    if outlet:
                        eq_result["outlet_temperature_K"] = outlet.getTemperature()
                        eq_result["outlet_pressure_bara"] = outlet.getPressure()
                        eq_result["outlet_flow_kg_hr"] = outlet.getFlowRate("kg/hr")
            except:
                pass
            
            try:
                if hasattr(eq_obj, "getPower"):
                    eq_result["power_W"] = eq_obj.getPower()
                    eq_result["power_MW"] = eq_obj.getPower() / 1e6
            except:
                pass
            
            try:
                if hasattr(eq_obj, "getDuty"):
                    eq_result["duty_W"] = eq_obj.getDuty()
                    eq_result["duty_MW"] = eq_obj.getDuty() / 1e6
            except:
                pass
            
            try:
                if hasattr(eq_obj, "getPolytropicEfficiency"):
                    eq_result["polytropic_efficiency"] = eq_obj.getPolytropicEfficiency()
                if hasattr(eq_obj, "getIsentropicEfficiency"):
                    eq_result["isentropic_efficiency"] = eq_obj.getIsentropicEfficiency()
            except:
                pass
                
            equipment_results[eq_name] = eq_result
        
        # Get full results as JSON
        try:
            full_results = process.results_json()
        except:
            full_results = None
        
        # Get stream data
        stream_data = None
        try:
            df = process.results_dataframe()
            stream_data = df.to_dict(orient="records")
        except:
            pass
        
        return SimulationResult(
            success=True,
            process_name=config.name or "Process",
            equipment_results=equipment_results,
            stream_data=stream_data,
        )
        
    except Exception as e:
        return SimulationResult(
            success=False,
            process_name=config.name or "Process",
            equipment_results={},
            error=f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
        )


@app.post("/flash", response_model=FlashResult)
async def run_flash(
    request: FlashRequest = Body(..., example={
        "fluid": {
            "model": "srk",
            "temperature": 303.15,
            "pressure": 50.0,
            "components": [
                {"name": "methane", "moles": 0.85},
                {"name": "ethane", "moles": 0.10},
                {"name": "propane", "moles": 0.05}
            ]
        },
        "temperature": 280.0,
        "pressure": 30.0
    })
):
    """
    Run a TP flash calculation on a fluid.
    
    Returns phase properties and compositions.
    """
    if not NEQSIM_AVAILABLE:
        raise HTTPException(status_code=503, detail=f"NeqSim not available: {NEQSIM_ERROR}")
    
    try:
        # Create fluid
        fluid_config = request.fluid.model_dump(exclude_none=True)
        fluid = create_fluid_from_config(fluid_config)
        
        # Set conditions
        if request.temperature:
            fluid.setTemperature(request.temperature)
        if request.pressure:
            fluid.setPressure(request.pressure)
        
        # Run flash
        TPflash(fluid)
        
        # Collect phase results
        phases = []
        for i in range(fluid.getNumberOfPhases()):
            phase = fluid.getPhase(i)
            phase_data = {
                "phase_number": i,
                "phase_type": str(phase.getPhaseTypeName()),
                "mole_fraction": fluid.getBeta(i),
                "temperature_K": phase.getTemperature(),
                "pressure_bara": phase.getPressure(),
                "density_kg_m3": phase.getDensity("kg/m3"),
                "molar_mass_kg_kmol": phase.getMolarMass() * 1000,
                "Z_factor": phase.getZ(),
                "viscosity_Pa_s": phase.getViscosity("kg/msec"),
                "components": {}
            }
            
            for j in range(phase.getNumberOfComponents()):
                comp = phase.getComponent(j)
                phase_data["components"][comp.getName()] = {
                    "mole_fraction": comp.getx(),
                    "fugacity_coefficient": comp.getFugacityCoefficient(),
                }
            
            phases.append(phase_data)
        
        # Overall properties
        properties = {
            "number_of_phases": fluid.getNumberOfPhases(),
            "enthalpy_J_mol": fluid.getEnthalpy() / fluid.getTotalNumberOfMoles(),
            "entropy_J_mol_K": fluid.getEntropy() / fluid.getTotalNumberOfMoles(),
        }
        
        return FlashResult(
            success=True,
            temperature=fluid.getTemperature(),
            pressure=fluid.getPressure(),
            phases=phases,
            properties=properties,
        )
        
    except Exception as e:
        return FlashResult(
            success=False,
            temperature=request.temperature or 0,
            pressure=request.pressure or 0,
            phases=[],
            properties={},
            error=f"{type(e).__name__}: {str(e)}"
        )


@app.post("/simulate/yaml")
async def run_simulation_yaml(yaml_content: str = Body(..., media_type="text/plain")):
    """
    Run a process simulation from YAML content.
    
    Send raw YAML as the request body with Content-Type: text/plain
    """
    if not NEQSIM_AVAILABLE:
        raise HTTPException(status_code=503, detail=f"NeqSim not available: {NEQSIM_ERROR}")
    
    try:
        import yaml
        config = yaml.safe_load(yaml_content)
        
        # Run simulation
        process = create_process_from_config(config, run=True)
        
        # Return results as JSON
        return {
            "success": True,
            "results": process.results_json()
        }
        
    except ImportError:
        raise HTTPException(status_code=500, detail="PyYAML not installed")
    except Exception as e:
        return {
            "success": False,
            "error": f"{type(e).__name__}: {str(e)}"
        }


# =============================================================================
# Main Entry Point
# =============================================================================


if __name__ == "__main__":
    import uvicorn
    print("Starting NeqSim Process Simulation API...")
    print("API documentation available at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
