"""
NeqSim Process Builder GUI

A simple graphical user interface for building and running process simulations.
Run with: streamlit run processBuilderGUI.py

Requires: pip install streamlit pandas
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, List

# Must be first Streamlit command
st.set_page_config(page_title="NeqSim Process Builder", layout="wide")

from neqsim.thermo import fluid
from neqsim.process import ProcessBuilder

# =============================================================================
# Session State Initialization
# =============================================================================

if "fluids" not in st.session_state:
    st.session_state.fluids = {}
if "equipment_list" not in st.session_state:
    st.session_state.equipment_list = []
if "process_result" not in st.session_state:
    st.session_state.process_result = None
if "results_data" not in st.session_state:
    st.session_state.results_data = None

# =============================================================================
# Helper Functions
# =============================================================================

COMPONENT_OPTIONS = [
    "methane",
    "ethane",
    "propane",
    "i-butane",
    "n-butane",
    "i-pentane",
    "n-pentane",
    "n-hexane",
    "n-heptane",
    "n-octane",
    "nitrogen",
    "CO2",
    "H2S",
    "water",
    "H2",
    "oxygen",
]

EOS_OPTIONS = ["srk", "pr", "cpa"]

EQUIPMENT_TYPES = {
    "stream": {"inlet": False, "has_fluid": True},
    "separator": {"inlet": True, "has_fluid": False},
    "compressor": {"inlet": True, "has_fluid": False},
    "pump": {"inlet": True, "has_fluid": False},
    "expander": {"inlet": True, "has_fluid": False},
    "valve": {"inlet": True, "has_fluid": False},
    "heater": {"inlet": True, "has_fluid": False},
    "cooler": {"inlet": True, "has_fluid": False},
    "pipe": {"inlet": True, "has_fluid": False},
}

FLOW_UNITS = ["kg/sec", "kg/hr", "MSm3/day", "Sm3/day", "mole/sec"]


def get_available_inlets() -> List[str]:
    """Get list of equipment names that can be used as inlets."""
    return [eq["name"] for eq in st.session_state.equipment_list]


def create_fluid_from_config(config: Dict) -> Any:
    """Create a NeqSim fluid from configuration."""
    f = fluid(config["eos"])
    for comp, frac in config["components"].items():
        if frac > 0:
            f.addComponent(comp, frac)
    f.setTemperature(config["temperature"], "C")
    f.setPressure(config["pressure"], "bara")
    if config.get("flow_rate"):
        f.setTotalFlowRate(config["flow_rate"], config.get("flow_unit", "kg/sec"))
    return f


def run_process():
    """Build and run the process from current configuration."""
    if not st.session_state.equipment_list:
        st.error("Add at least one piece of equipment before running")
        return

    # Create fluids
    fluids_dict = {}
    for name, config in st.session_state.fluids.items():
        fluids_dict[name] = create_fluid_from_config(config)

    # Build equipment config
    equipment_config = []
    for eq in st.session_state.equipment_list:
        eq_config = {"type": eq["type"], "name": eq["name"]}
        eq_config.update(eq.get("params", {}))
        equipment_config.append(eq_config)

    config = {"name": "GUI Process", "equipment": equipment_config}

    try:
        process = ProcessBuilder.from_dict(config, fluids=fluids_dict).run()
        st.session_state.process_result = process

        # Collect results
        results = []
        for eq in st.session_state.equipment_list:
            name = eq["name"]
            eq_obj = process.get(name)
            if eq_obj:
                result = {"Equipment": name, "Type": eq["type"]}

                # Try to get common properties
                if hasattr(eq_obj, "getOutletStream"):
                    out = eq_obj.getOutletStream()
                    result["Outlet T (°C)"] = f"{out.getTemperature() - 273.15:.1f}"
                    result["Outlet P (bara)"] = f"{out.getPressure():.1f}"
                elif hasattr(eq_obj, "getOutStream"):
                    out = eq_obj.getOutStream()
                    result["Outlet T (°C)"] = f"{out.getTemperature() - 273.15:.1f}"
                    result["Outlet P (bara)"] = f"{out.getPressure():.1f}"
                elif hasattr(eq_obj, "getGasOutStream"):
                    out = eq_obj.getGasOutStream()
                    result["Outlet T (°C)"] = f"{out.getTemperature() - 273.15:.1f}"
                    result["Outlet P (bara)"] = f"{out.getPressure():.1f}"

                if hasattr(eq_obj, "getPower"):
                    power = eq_obj.getPower()
                    result["Power (kW)"] = f"{power/1e3:.1f}"

                if hasattr(eq_obj, "getDuty"):
                    duty = eq_obj.getDuty()
                    result["Duty (kW)"] = f"{duty/1e3:.1f}"

                results.append(result)

        st.session_state.results_data = pd.DataFrame(results)
        st.success("Process simulation completed!")

    except Exception as e:
        st.error(f"Error running process: {str(e)}")


# =============================================================================
# Main UI
# =============================================================================

st.title("🔧 NeqSim Process Builder")
st.markdown("Build and simulate process systems with a visual interface")

# Create tabs
tab1, tab2, tab3 = st.tabs(["📦 Define Fluids", "🏭 Build Process", "📊 Results"])

# =============================================================================
# Tab 1: Define Fluids
# =============================================================================

with tab1:
    st.header("Define Fluids")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Create New Fluid")

        fluid_name = st.text_input("Fluid Name", value="feed", key="new_fluid_name")
        eos = st.selectbox("Equation of State", EOS_OPTIONS)

        st.markdown("**Composition (mole fractions)**")
        components = {}
        cols = st.columns(2)
        for i, comp in enumerate(COMPONENT_OPTIONS[:10]):
            with cols[i % 2]:
                val = st.number_input(
                    comp,
                    min_value=0.0,
                    max_value=1.0,
                    value=(
                        0.9 if comp == "methane" else 0.1 if comp == "ethane" else 0.0
                    ),
                    step=0.01,
                    key=f"comp_{comp}",
                )
                if val > 0:
                    components[comp] = val

        st.markdown("**Conditions**")
        temperature = st.number_input("Temperature (°C)", value=30.0)
        pressure = st.number_input("Pressure (bara)", value=50.0, min_value=0.1)

        st.markdown("**Flow Rate (optional)**")
        flow_rate = st.number_input("Flow Rate", value=10.0, min_value=0.0)
        flow_unit = st.selectbox("Flow Unit", FLOW_UNITS, index=2)

        if st.button("➕ Add Fluid", type="primary"):
            if fluid_name and components:
                st.session_state.fluids[fluid_name] = {
                    "eos": eos,
                    "components": components,
                    "temperature": temperature,
                    "pressure": pressure,
                    "flow_rate": flow_rate if flow_rate > 0 else None,
                    "flow_unit": flow_unit,
                }
                st.success(f"Fluid '{fluid_name}' added!")
                st.rerun()

    with col2:
        st.subheader("Defined Fluids")
        if st.session_state.fluids:
            for name, config in st.session_state.fluids.items():
                with st.expander(f"📦 {name}", expanded=True):
                    st.write(f"**EOS:** {config['eos']}")
                    st.write(
                        f"**T:** {config['temperature']} °C | **P:** {config['pressure']} bara"
                    )
                    if config.get("flow_rate"):
                        st.write(
                            f"**Flow:** {config['flow_rate']} {config['flow_unit']}"
                        )
                    st.write("**Composition:**", config["components"])
                    if st.button(f"🗑️ Remove", key=f"del_fluid_{name}"):
                        del st.session_state.fluids[name]
                        st.rerun()
        else:
            st.info("No fluids defined yet. Create one using the form on the left.")

# =============================================================================
# Tab 2: Build Process
# =============================================================================

with tab2:
    st.header("Build Process")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Add Equipment")

        eq_type = st.selectbox("Equipment Type", list(EQUIPMENT_TYPES.keys()))
        eq_name = st.text_input("Equipment Name", value=f"{eq_type}_1")

        params = {}

        # Equipment-specific parameters
        if EQUIPMENT_TYPES[eq_type]["has_fluid"]:
            if st.session_state.fluids:
                params["fluid"] = st.selectbox(
                    "Select Fluid", list(st.session_state.fluids.keys())
                )
            else:
                st.warning("Define a fluid first in the 'Define Fluids' tab")

        if EQUIPMENT_TYPES[eq_type]["inlet"]:
            inlets = get_available_inlets()
            if inlets:
                params["inlet"] = st.selectbox("Inlet From", inlets)
            else:
                st.warning("Add a stream first")

        if eq_type == "compressor":
            params["pressure"] = st.number_input(
                "Outlet Pressure (bara)", value=100.0, min_value=0.1
            )
            params["efficiency"] = st.slider("Isentropic Efficiency", 0.5, 1.0, 0.75)

        elif eq_type == "pump":
            params["pressure"] = st.number_input(
                "Outlet Pressure (bara)", value=100.0, min_value=0.1
            )
            params["efficiency"] = st.slider("Efficiency", 0.5, 1.0, 0.75)

        elif eq_type == "expander":
            params["pressure"] = st.number_input(
                "Outlet Pressure (bara)", value=10.0, min_value=0.1
            )

        elif eq_type == "valve":
            params["pressure"] = st.number_input(
                "Outlet Pressure (bara)", value=10.0, min_value=0.1
            )

        elif eq_type == "heater":
            params["temperature"] = st.number_input(
                "Outlet Temperature (K)", value=350.0
            )

        elif eq_type == "cooler":
            params["temperature"] = st.number_input(
                "Outlet Temperature (K)", value=300.0
            )

        elif eq_type == "separator":
            params["three_phase"] = st.checkbox("Three-phase separator")

        elif eq_type == "pipe":
            params["length"] = st.number_input("Length (m)", value=100.0)
            params["diameter"] = st.number_input("Diameter (m)", value=0.1)

        # Add button
        can_add = True
        if EQUIPMENT_TYPES[eq_type]["inlet"] and not get_available_inlets():
            can_add = False
        if EQUIPMENT_TYPES[eq_type]["has_fluid"] and not st.session_state.fluids:
            can_add = False

        if st.button("➕ Add Equipment", type="primary", disabled=not can_add):
            st.session_state.equipment_list.append(
                {"type": eq_type, "name": eq_name, "params": params}
            )
            st.success(f"Added {eq_type} '{eq_name}'")
            st.rerun()

    with col2:
        st.subheader("Process Equipment")

        if st.session_state.equipment_list:
            for i, eq in enumerate(st.session_state.equipment_list):
                with st.expander(
                    f"{'🔵' if eq['type'] == 'stream' else '⚙️'} {eq['name']} ({eq['type']})",
                    expanded=True,
                ):
                    for key, value in eq["params"].items():
                        st.write(f"**{key}:** {value}")

                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("⬆️ Move Up", key=f"up_{i}", disabled=i == 0):
                            (
                                st.session_state.equipment_list[i],
                                st.session_state.equipment_list[i - 1],
                            ) = (
                                st.session_state.equipment_list[i - 1],
                                st.session_state.equipment_list[i],
                            )
                            st.rerun()
                    with col_b:
                        if st.button("🗑️ Remove", key=f"del_{i}"):
                            st.session_state.equipment_list.pop(i)
                            st.rerun()

            st.divider()

            col_run, col_clear = st.columns(2)
            with col_run:
                if st.button(
                    "▶️ Run Simulation", type="primary", use_container_width=True
                ):
                    run_process()
            with col_clear:
                if st.button("🗑️ Clear All", use_container_width=True):
                    st.session_state.equipment_list = []
                    st.session_state.process_result = None
                    st.session_state.results_data = None
                    st.rerun()
        else:
            st.info(
                "No equipment added yet. Use the form on the left to add equipment."
            )

# =============================================================================
# Tab 3: Results
# =============================================================================

with tab3:
    st.header("Simulation Results")

    if st.session_state.results_data is not None:
        st.dataframe(st.session_state.results_data, use_container_width=True)

        # Show detailed results for each equipment
        st.subheader("Detailed Equipment Results")

        if st.session_state.process_result:
            for eq in st.session_state.equipment_list:
                eq_obj = st.session_state.process_result.get(eq["name"])
                if eq_obj:
                    with st.expander(f"📋 {eq['name']} Details"):
                        # Get outlet stream properties
                        out_stream = None
                        if hasattr(eq_obj, "getOutletStream"):
                            out_stream = eq_obj.getOutletStream()
                        elif hasattr(eq_obj, "getOutStream"):
                            out_stream = eq_obj.getOutStream()
                        elif hasattr(eq_obj, "getGasOutStream"):
                            out_stream = eq_obj.getGasOutStream()

                        if out_stream:
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric(
                                    "Temperature",
                                    f"{out_stream.getTemperature() - 273.15:.1f} °C",
                                )
                            with col2:
                                st.metric(
                                    "Pressure", f"{out_stream.getPressure():.1f} bara"
                                )
                            with col3:
                                try:
                                    st.metric(
                                        "Flow Rate",
                                        f"{out_stream.getFlowRate('kg/hr'):.0f} kg/hr",
                                    )
                                except:
                                    pass

                        if hasattr(eq_obj, "getPower"):
                            st.metric("Power", f"{eq_obj.getPower()/1e3:.2f} kW")
                        if hasattr(eq_obj, "getDuty"):
                            st.metric("Duty", f"{eq_obj.getDuty()/1e3:.2f} kW")

        # Export config button
        st.subheader("Export Configuration")

        equipment_config = []
        for eq in st.session_state.equipment_list:
            eq_config = {"type": eq["type"], "name": eq["name"]}
            eq_config.update(eq.get("params", {}))
            equipment_config.append(eq_config)

        config = {"name": "Exported Process", "equipment": equipment_config}

        import json

        json_str = json.dumps(config, indent=2)
        st.download_button(
            label="📥 Download JSON Config",
            data=json_str,
            file_name="process_config.json",
            mime="application/json",
        )

        st.code(json_str, language="json")
    else:
        st.info("Run a simulation to see results here.")

# =============================================================================
# Sidebar
# =============================================================================

with st.sidebar:
    st.header("ℹ️ About")
    st.markdown(
        """
    **NeqSim Process Builder GUI**

    A visual tool for building and simulating
    process systems using NeqSim.

    **Workflow:**
    1. Define fluids with compositions
    2. Add process equipment
    3. Run simulation
    4. View and export results

    **Supported Equipment:**
    - Streams
    - Separators (2/3 phase)
    - Compressors
    - Pumps
    - Expanders
    - Valves
    - Heaters/Coolers
    - Pipes
    """
    )

    st.divider()

    if st.button("🔄 Reset All"):
        st.session_state.fluids = {}
        st.session_state.equipment_list = []
        st.session_state.process_result = None
        st.session_state.results_data = None
        st.rerun()
