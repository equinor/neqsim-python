import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import java.util
import jneqsim.mcp.model
import typing

class AgenticEngineeringRunner:
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class AutomationRunner:
    @staticmethod
    def compareStates(
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
    ) -> java.lang.String: ...
    @staticmethod
    def diagnose(
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
        string3: typing.Union[java.lang.String, str],
    ) -> java.lang.String: ...
    @staticmethod
    def getAdjustableParameters(
        string: typing.Union[java.lang.String, str],
    ) -> java.lang.String: ...
    @staticmethod
    def getLearningReport(
        string: typing.Union[java.lang.String, str],
    ) -> java.lang.String: ...
    @staticmethod
    def getVariable(
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
        string3: typing.Union[java.lang.String, str],
    ) -> java.lang.String: ...
    @staticmethod
    def listUnits(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...
    @staticmethod
    def listVariables(
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
    ) -> java.lang.String: ...
    @staticmethod
    def runLoop(
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
        string3: typing.Union[java.lang.String, str],
        string4: typing.Union[java.lang.String, str],
        string5: typing.Union[java.lang.String, str],
    ) -> java.lang.String: ...
    @staticmethod
    def saveState(
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
        string3: typing.Union[java.lang.String, str],
    ) -> java.lang.String: ...
    @staticmethod
    def setVariableAndRun(
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
        double: float,
        string3: typing.Union[java.lang.String, str],
    ) -> java.lang.String: ...

class BarrierRegisterRunner:
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class BatchRunner:
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class BenchmarkTrust:
    @staticmethod
    def getMaturityLevel(
        string: typing.Union[java.lang.String, str],
    ) -> java.lang.String: ...
    @staticmethod
    def getToolTrust(
        string: typing.Union[java.lang.String, str],
    ) -> java.lang.String: ...
    @staticmethod
    def getTrustReport() -> java.lang.String: ...

    class MaturityLevel(java.lang.Enum["BenchmarkTrust.MaturityLevel"]):
        VALIDATED: typing.ClassVar["BenchmarkTrust.MaturityLevel"] = ...
        TESTED: typing.ClassVar["BenchmarkTrust.MaturityLevel"] = ...
        EXPERIMENTAL: typing.ClassVar["BenchmarkTrust.MaturityLevel"] = ...
        _valueOf_0__T = typing.TypeVar("_valueOf_0__T", bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(
            class_: typing.Type[_valueOf_0__T],
            string: typing.Union[java.lang.String, str],
        ) -> _valueOf_0__T: ...
        @typing.overload
        @staticmethod
        def valueOf(
            string: typing.Union[java.lang.String, str],
        ) -> "BenchmarkTrust.MaturityLevel": ...
        @staticmethod
        def values() -> typing.MutableSequence["BenchmarkTrust.MaturityLevel"]: ...

class BioprocessRunner:
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class CapabilitiesRunner:
    @staticmethod
    def getCapabilities() -> java.lang.String: ...
    @staticmethod
    def getSetupTemplate(
        string: typing.Union[java.lang.String, str],
    ) -> java.lang.String: ...
    @staticmethod
    def getSetupTemplates() -> java.lang.String: ...

class ChemistryRunner:
    @staticmethod
    def getSupportedAnalyses() -> java.util.List[java.lang.String]: ...
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class ComponentQuery:
    @staticmethod
    def closestMatch(
        string: typing.Union[java.lang.String, str],
    ) -> java.lang.String: ...
    @staticmethod
    def getAllNames() -> java.util.List[java.lang.String]: ...
    @staticmethod
    def getInfo(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...
    @staticmethod
    def isValid(string: typing.Union[java.lang.String, str]) -> bool: ...
    @staticmethod
    def search(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class CompositionRunner:
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class CrossValidationRunner:
    @staticmethod
    def crossValidate(
        string: typing.Union[java.lang.String, str],
    ) -> java.lang.String: ...

class DataCatalogRunner:
    @staticmethod
    def getComponentProperties(
        string: typing.Union[java.lang.String, str],
    ) -> java.lang.String: ...
    @staticmethod
    def listComponentFamilies() -> java.lang.String: ...
    @staticmethod
    def listDataTables() -> java.lang.String: ...
    @staticmethod
    def listDesignStandards() -> java.lang.String: ...
    @staticmethod
    def listEOSModels() -> java.lang.String: ...
    @staticmethod
    def listMaterials(
        string: typing.Union[java.lang.String, str],
    ) -> java.lang.String: ...
    @staticmethod
    def queryStandard(
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
    ) -> java.lang.String: ...
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class DynamicRunner:
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class EngineeringValidator:
    @staticmethod
    def validate(
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
    ) -> java.lang.String: ...
    @staticmethod
    def validateEquipment(
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
    ) -> java.lang.String: ...

class EquipmentSizingRunner:
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class FieldDevelopmentRunner:
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class FlareRadiationRunner:
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class FlashRunner:
    @staticmethod
    def getSupportedFlashTypes() -> java.util.List[java.lang.String]: ...
    @staticmethod
    def getSupportedModels() -> java.util.List[java.lang.String]: ...
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...
    @staticmethod
    def runTyped(
        flashRequest: jneqsim.mcp.model.FlashRequest,
    ) -> jneqsim.mcp.model.ApiEnvelope[jneqsim.mcp.model.FlashResult]: ...

class FlowAssuranceRunner:
    @staticmethod
    def getSupportedAnalyses() -> java.util.List[java.lang.String]: ...
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class HAZOPStudyRunner:
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class IndustrialProfile:
    @staticmethod
    def approveNextInvocation(
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
    ) -> java.lang.String: ...
    @staticmethod
    def describeProfiles() -> java.lang.String: ...
    @staticmethod
    def enforceAccess(
        string: typing.Union[java.lang.String, str],
    ) -> java.lang.String: ...
    @staticmethod
    def getActiveMode() -> "IndustrialProfile.DeploymentMode": ...
    @staticmethod
    def getEngineeringAdvanced() -> java.util.Set[java.lang.String]: ...
    @staticmethod
    def getExperimentalTools() -> java.util.Set[java.lang.String]: ...
    @staticmethod
    def getIndustrialCore() -> java.util.Set[java.lang.String]: ...
    @staticmethod
    def getToolCategory(
        string: typing.Union[java.lang.String, str],
    ) -> "IndustrialProfile.ToolCategory": ...
    @staticmethod
    def getToolTier(
        string: typing.Union[java.lang.String, str],
    ) -> "IndustrialProfile.ToolTier": ...
    @staticmethod
    def isAdminAuthorized(string: typing.Union[java.lang.String, str]) -> bool: ...
    @staticmethod
    def isAdminConfigured() -> bool: ...
    @staticmethod
    def isAutoValidationEnabled() -> bool: ...
    @staticmethod
    def isToolAllowed(string: typing.Union[java.lang.String, str]) -> bool: ...
    @staticmethod
    def requiresApproval(string: typing.Union[java.lang.String, str]) -> bool: ...
    @staticmethod
    def setActiveMode(deploymentMode: "IndustrialProfile.DeploymentMode") -> None: ...

    class DeploymentMode(java.lang.Enum["IndustrialProfile.DeploymentMode"]):
        DESKTOP_ENGINEER: typing.ClassVar["IndustrialProfile.DeploymentMode"] = ...
        STUDY_TEAM: typing.ClassVar["IndustrialProfile.DeploymentMode"] = ...
        DIGITAL_TWIN: typing.ClassVar["IndustrialProfile.DeploymentMode"] = ...
        ENTERPRISE: typing.ClassVar["IndustrialProfile.DeploymentMode"] = ...
        _valueOf_0__T = typing.TypeVar("_valueOf_0__T", bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(
            class_: typing.Type[_valueOf_0__T],
            string: typing.Union[java.lang.String, str],
        ) -> _valueOf_0__T: ...
        @typing.overload
        @staticmethod
        def valueOf(
            string: typing.Union[java.lang.String, str],
        ) -> "IndustrialProfile.DeploymentMode": ...
        @staticmethod
        def values() -> typing.MutableSequence["IndustrialProfile.DeploymentMode"]: ...

    class ToolCategory(java.lang.Enum["IndustrialProfile.ToolCategory"]):
        ADVISORY: typing.ClassVar["IndustrialProfile.ToolCategory"] = ...
        CALCULATION: typing.ClassVar["IndustrialProfile.ToolCategory"] = ...
        EXECUTION: typing.ClassVar["IndustrialProfile.ToolCategory"] = ...
        PLATFORM: typing.ClassVar["IndustrialProfile.ToolCategory"] = ...
        _valueOf_0__T = typing.TypeVar("_valueOf_0__T", bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(
            class_: typing.Type[_valueOf_0__T],
            string: typing.Union[java.lang.String, str],
        ) -> _valueOf_0__T: ...
        @typing.overload
        @staticmethod
        def valueOf(
            string: typing.Union[java.lang.String, str],
        ) -> "IndustrialProfile.ToolCategory": ...
        @staticmethod
        def values() -> typing.MutableSequence["IndustrialProfile.ToolCategory"]: ...

    class ToolTier(java.lang.Enum["IndustrialProfile.ToolTier"]):
        TRUSTED_CORE: typing.ClassVar["IndustrialProfile.ToolTier"] = ...
        ENGINEERING_ADVANCED: typing.ClassVar["IndustrialProfile.ToolTier"] = ...
        EXPERIMENTAL: typing.ClassVar["IndustrialProfile.ToolTier"] = ...
        _valueOf_0__T = typing.TypeVar("_valueOf_0__T", bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(
            class_: typing.Type[_valueOf_0__T],
            string: typing.Union[java.lang.String, str],
        ) -> _valueOf_0__T: ...
        @typing.overload
        @staticmethod
        def valueOf(
            string: typing.Union[java.lang.String, str],
        ) -> "IndustrialProfile.ToolTier": ...
        @staticmethod
        def values() -> typing.MutableSequence["IndustrialProfile.ToolTier"]: ...

class LOPARunner:
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class MaterialsReviewRunner:
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class McpRunnerPlugin:
    def description(self) -> java.lang.String: ...
    def inputSchema(self) -> java.lang.String: ...
    def name(self) -> java.lang.String: ...
    def run(self, string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class NorsokS001Clause10ReviewRunner:
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class OpenDrainReviewRunner:
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class OperationalStudyRunner:
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class PVTRunner:
    @staticmethod
    def getSupportedExperiments() -> java.util.List[java.lang.String]: ...
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class ParametricStudyRunner:
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class PhaseEnvelopeRunner:
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class PipelineRunner:
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class PluginRegistry:
    @staticmethod
    def clear() -> None: ...
    @staticmethod
    def get(string: typing.Union[java.lang.String, str]) -> McpRunnerPlugin: ...
    @staticmethod
    def has(string: typing.Union[java.lang.String, str]) -> bool: ...
    @staticmethod
    def listNames() -> java.util.List[java.lang.String]: ...
    @staticmethod
    def listPlugins() -> java.lang.String: ...
    @staticmethod
    def register(mcpRunnerPlugin: McpRunnerPlugin) -> None: ...
    @staticmethod
    def runPlugin(
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
    ) -> java.lang.String: ...
    @staticmethod
    def size() -> int: ...
    @staticmethod
    def unregister(string: typing.Union[java.lang.String, str]) -> McpRunnerPlugin: ...

class ProcessComparisonRunner:
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class ProcessRunner:
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...
    @staticmethod
    def runTyped(
        string: typing.Union[java.lang.String, str],
    ) -> jneqsim.mcp.model.ApiEnvelope[jneqsim.mcp.model.ProcessResult]: ...
    @staticmethod
    def validateAndRun(
        string: typing.Union[java.lang.String, str],
    ) -> java.lang.String: ...

class ProgressTracker:
    @staticmethod
    def complete(
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
    ) -> None: ...
    @staticmethod
    def fail(
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
    ) -> None: ...
    @staticmethod
    def getProgress(
        string: typing.Union[java.lang.String, str],
    ) -> java.lang.String: ...
    @staticmethod
    def listActive() -> java.lang.String: ...
    @staticmethod
    def start(
        string: typing.Union[java.lang.String, str], int: int
    ) -> java.lang.String: ...
    @staticmethod
    def update(
        string: typing.Union[java.lang.String, str],
        int: int,
        string2: typing.Union[java.lang.String, str],
    ) -> None: ...

class PropertyTableRunner:
    @staticmethod
    def getAvailableProperties() -> java.util.List[java.lang.String]: ...
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class ReliefRunner:
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class ReportRunner:
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class ReservoirRunner:
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class RiskMatrixRunner:
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class RootCauseRunner:
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class SILRunner:
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class SafetySystemPerformanceRunner:
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class SecurityRunner:
    @staticmethod
    def checkAccess(
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
    ) -> java.lang.String: ...
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class SessionRunner:
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class StandardsRunner:
    @staticmethod
    def getSupportedStandards() -> java.util.List[java.lang.String]: ...
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class StatePersistenceRunner:
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class StreamingRunner:
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class TaskSolverRunner:
    @staticmethod
    def composeWorkflow(
        string: typing.Union[java.lang.String, str],
    ) -> java.lang.String: ...
    @staticmethod
    def solveTask(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class TaskWorkflowBridge:
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class ValidationProfileRunner:
    @staticmethod
    def getActiveProfile() -> java.lang.String: ...
    @staticmethod
    def getActiveProfileName() -> java.lang.String: ...
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class Validator:
    @staticmethod
    def validate(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class VisualizationRunner:
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class WaterHammerRunner:
    @staticmethod
    def run(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.mcp.runners")``.

    AgenticEngineeringRunner: typing.Type[AgenticEngineeringRunner]
    AutomationRunner: typing.Type[AutomationRunner]
    BarrierRegisterRunner: typing.Type[BarrierRegisterRunner]
    BatchRunner: typing.Type[BatchRunner]
    BenchmarkTrust: typing.Type[BenchmarkTrust]
    BioprocessRunner: typing.Type[BioprocessRunner]
    CapabilitiesRunner: typing.Type[CapabilitiesRunner]
    ChemistryRunner: typing.Type[ChemistryRunner]
    ComponentQuery: typing.Type[ComponentQuery]
    CompositionRunner: typing.Type[CompositionRunner]
    CrossValidationRunner: typing.Type[CrossValidationRunner]
    DataCatalogRunner: typing.Type[DataCatalogRunner]
    DynamicRunner: typing.Type[DynamicRunner]
    EngineeringValidator: typing.Type[EngineeringValidator]
    EquipmentSizingRunner: typing.Type[EquipmentSizingRunner]
    FieldDevelopmentRunner: typing.Type[FieldDevelopmentRunner]
    FlareRadiationRunner: typing.Type[FlareRadiationRunner]
    FlashRunner: typing.Type[FlashRunner]
    FlowAssuranceRunner: typing.Type[FlowAssuranceRunner]
    HAZOPStudyRunner: typing.Type[HAZOPStudyRunner]
    IndustrialProfile: typing.Type[IndustrialProfile]
    LOPARunner: typing.Type[LOPARunner]
    MaterialsReviewRunner: typing.Type[MaterialsReviewRunner]
    McpRunnerPlugin: typing.Type[McpRunnerPlugin]
    NorsokS001Clause10ReviewRunner: typing.Type[NorsokS001Clause10ReviewRunner]
    OpenDrainReviewRunner: typing.Type[OpenDrainReviewRunner]
    OperationalStudyRunner: typing.Type[OperationalStudyRunner]
    PVTRunner: typing.Type[PVTRunner]
    ParametricStudyRunner: typing.Type[ParametricStudyRunner]
    PhaseEnvelopeRunner: typing.Type[PhaseEnvelopeRunner]
    PipelineRunner: typing.Type[PipelineRunner]
    PluginRegistry: typing.Type[PluginRegistry]
    ProcessComparisonRunner: typing.Type[ProcessComparisonRunner]
    ProcessRunner: typing.Type[ProcessRunner]
    ProgressTracker: typing.Type[ProgressTracker]
    PropertyTableRunner: typing.Type[PropertyTableRunner]
    ReliefRunner: typing.Type[ReliefRunner]
    ReportRunner: typing.Type[ReportRunner]
    ReservoirRunner: typing.Type[ReservoirRunner]
    RiskMatrixRunner: typing.Type[RiskMatrixRunner]
    RootCauseRunner: typing.Type[RootCauseRunner]
    SILRunner: typing.Type[SILRunner]
    SafetySystemPerformanceRunner: typing.Type[SafetySystemPerformanceRunner]
    SecurityRunner: typing.Type[SecurityRunner]
    SessionRunner: typing.Type[SessionRunner]
    StandardsRunner: typing.Type[StandardsRunner]
    StatePersistenceRunner: typing.Type[StatePersistenceRunner]
    StreamingRunner: typing.Type[StreamingRunner]
    TaskSolverRunner: typing.Type[TaskSolverRunner]
    TaskWorkflowBridge: typing.Type[TaskWorkflowBridge]
    ValidationProfileRunner: typing.Type[ValidationProfileRunner]
    Validator: typing.Type[Validator]
    VisualizationRunner: typing.Type[VisualizationRunner]
    WaterHammerRunner: typing.Type[WaterHammerRunner]
