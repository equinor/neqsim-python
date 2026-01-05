import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import java.nio.file
import java.time
import java.util
import java.util.function
import jpype.protocol
import jneqsim.process.equipment
import jneqsim.process.equipment.stream
import jneqsim.process.processmodel
import typing

class BatchStudy(java.io.Serializable):
    @staticmethod
    def builder(
        processSystem: jneqsim.process.processmodel.ProcessSystem,
    ) -> "BatchStudy.Builder": ...
    def getTotalCases(self) -> int: ...
    def run(self) -> "BatchStudy.BatchStudyResult": ...

    class BatchStudyResult(java.io.Serializable):
        def exportToCSV(self, string: typing.Union[java.lang.String, str]) -> None: ...
        def exportToJSON(self, string: typing.Union[java.lang.String, str]) -> None: ...
        def getAllResults(self) -> java.util.List["BatchStudy.CaseResult"]: ...
        def getBestCase(
            self, string: typing.Union[java.lang.String, str]
        ) -> "BatchStudy.CaseResult": ...
        def getFailureCount(self) -> int: ...
        def getParetoFront(
            self,
            string: typing.Union[java.lang.String, str],
            string2: typing.Union[java.lang.String, str],
        ) -> java.util.List["BatchStudy.CaseResult"]: ...
        def getSuccessCount(self) -> int: ...
        def getSuccessfulResults(self) -> java.util.List["BatchStudy.CaseResult"]: ...
        def getSummary(self) -> java.lang.String: ...
        def getTotalCases(self) -> int: ...
        def toJson(self) -> java.lang.String: ...

    class Builder:
        def addObjective(
            self,
            string: typing.Union[java.lang.String, str],
            objective: "BatchStudy.Objective",
            function: typing.Union[
                java.util.function.Function[
                    jneqsim.process.processmodel.ProcessSystem, float
                ],
                typing.Callable[[jneqsim.process.processmodel.ProcessSystem], float],
            ],
        ) -> "BatchStudy.Builder": ...
        def build(self) -> "BatchStudy": ...
        def name(
            self, string: typing.Union[java.lang.String, str]
        ) -> "BatchStudy.Builder": ...
        def parallelism(self, int: int) -> "BatchStudy.Builder": ...
        def stopOnFailure(self, boolean: bool) -> "BatchStudy.Builder": ...
        @typing.overload
        def vary(
            self,
            string: typing.Union[java.lang.String, str],
            double: float,
            double2: float,
            int: int,
        ) -> "BatchStudy.Builder": ...
        @typing.overload
        def vary(
            self, string: typing.Union[java.lang.String, str], *double: float
        ) -> "BatchStudy.Builder": ...

    class CaseResult(java.io.Serializable):
        parameters: "BatchStudy.ParameterSet" = ...
        failed: bool = ...
        errorMessage: java.lang.String = ...
        objectiveValues: java.util.Map = ...
        runtime: java.time.Duration = ...
        def __init__(
            self,
            parameterSet: "BatchStudy.ParameterSet",
            boolean: bool,
            string: typing.Union[java.lang.String, str],
        ): ...

    class Objective(java.lang.Enum["BatchStudy.Objective"]):
        MINIMIZE: typing.ClassVar["BatchStudy.Objective"] = ...
        MAXIMIZE: typing.ClassVar["BatchStudy.Objective"] = ...
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
            string: typing.Union[java.lang.String, str]
        ) -> "BatchStudy.Objective": ...
        @staticmethod
        def values() -> typing.MutableSequence["BatchStudy.Objective"]: ...

    class ObjectiveDefinition(java.io.Serializable):
        name: java.lang.String = ...
        direction: "BatchStudy.Objective" = ...
        def __init__(
            self,
            string: typing.Union[java.lang.String, str],
            objective: "BatchStudy.Objective",
        ): ...

    class ParameterSet(java.io.Serializable):
        caseId: java.lang.String = ...
        values: java.util.Map = ...
        def __init__(
            self,
            map: typing.Union[
                java.util.Map[typing.Union[java.lang.String, str], float],
                typing.Mapping[typing.Union[java.lang.String, str], float],
            ],
        ): ...
        def toString(self) -> java.lang.String: ...

class ProductionOptimizationSpecLoader:
    @staticmethod
    def load(
        path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath],
        map: typing.Union[
            java.util.Map[
                typing.Union[java.lang.String, str],
                jneqsim.process.processmodel.ProcessSystem,
            ],
            typing.Mapping[
                typing.Union[java.lang.String, str],
                jneqsim.process.processmodel.ProcessSystem,
            ],
        ],
        map2: typing.Union[
            java.util.Map[
                typing.Union[java.lang.String, str],
                jneqsim.process.equipment.stream.StreamInterface,
            ],
            typing.Mapping[
                typing.Union[java.lang.String, str],
                jneqsim.process.equipment.stream.StreamInterface,
            ],
        ],
        map3: typing.Union[
            java.util.Map[
                typing.Union[java.lang.String, str],
                typing.Union[
                    java.util.function.ToDoubleFunction[
                        jneqsim.process.processmodel.ProcessSystem
                    ],
                    typing.Callable[
                        [jneqsim.process.processmodel.ProcessSystem], float
                    ],
                ],
            ],
            typing.Mapping[
                typing.Union[java.lang.String, str],
                typing.Union[
                    java.util.function.ToDoubleFunction[
                        jneqsim.process.processmodel.ProcessSystem
                    ],
                    typing.Callable[
                        [jneqsim.process.processmodel.ProcessSystem], float
                    ],
                ],
            ],
        ],
    ) -> java.util.List["ProductionOptimizer.ScenarioRequest"]: ...

class ProductionOptimizer:
    DEFAULT_UTILIZATION_LIMIT: typing.ClassVar[float] = ...
    def __init__(self): ...
    @staticmethod
    def buildUtilizationSeries(
        list: java.util.List["ProductionOptimizer.IterationRecord"],
    ) -> java.util.List["ProductionOptimizer.UtilizationSeries"]: ...
    def compareScenarios(
        self,
        list: java.util.List["ProductionOptimizer.ScenarioRequest"],
        list2: java.util.List["ProductionOptimizer.ScenarioKpi"],
    ) -> "ProductionOptimizer.ScenarioComparisonResult": ...
    @staticmethod
    def formatScenarioComparisonTable(
        scenarioComparisonResult: "ProductionOptimizer.ScenarioComparisonResult",
        list: java.util.List["ProductionOptimizer.ScenarioKpi"],
    ) -> java.lang.String: ...
    @staticmethod
    def formatUtilizationTable(
        list: java.util.List["ProductionOptimizer.UtilizationRecord"],
    ) -> java.lang.String: ...
    @staticmethod
    def formatUtilizationTimeline(
        list: java.util.List["ProductionOptimizer.IterationRecord"],
    ) -> java.lang.String: ...
    @typing.overload
    def optimize(
        self,
        processSystem: jneqsim.process.processmodel.ProcessSystem,
        list: java.util.List["ProductionOptimizer.ManipulatedVariable"],
        optimizationConfig: "ProductionOptimizer.OptimizationConfig",
        list2: java.util.List["ProductionOptimizer.OptimizationObjective"],
        list3: java.util.List["ProductionOptimizer.OptimizationConstraint"],
    ) -> "ProductionOptimizer.OptimizationResult": ...
    @typing.overload
    def optimize(
        self,
        processSystem: jneqsim.process.processmodel.ProcessSystem,
        streamInterface: jneqsim.process.equipment.stream.StreamInterface,
        optimizationConfig: "ProductionOptimizer.OptimizationConfig",
        list: java.util.List["ProductionOptimizer.OptimizationObjective"],
        list2: java.util.List["ProductionOptimizer.OptimizationConstraint"],
    ) -> "ProductionOptimizer.OptimizationResult": ...
    def optimizeScenarios(
        self, list: java.util.List["ProductionOptimizer.ScenarioRequest"]
    ) -> java.util.List["ProductionOptimizer.ScenarioResult"]: ...
    def optimizeThroughput(
        self,
        processSystem: jneqsim.process.processmodel.ProcessSystem,
        streamInterface: jneqsim.process.equipment.stream.StreamInterface,
        double: float,
        double2: float,
        string: typing.Union[java.lang.String, str],
        list: java.util.List["ProductionOptimizer.OptimizationConstraint"],
    ) -> "ProductionOptimizer.OptimizationResult": ...
    @typing.overload
    def quickOptimize(
        self,
        processSystem: jneqsim.process.processmodel.ProcessSystem,
        streamInterface: jneqsim.process.equipment.stream.StreamInterface,
    ) -> "ProductionOptimizer.OptimizationSummary": ...
    @typing.overload
    def quickOptimize(
        self,
        processSystem: jneqsim.process.processmodel.ProcessSystem,
        streamInterface: jneqsim.process.equipment.stream.StreamInterface,
        string: typing.Union[java.lang.String, str],
        list: java.util.List["ProductionOptimizer.OptimizationConstraint"],
    ) -> "ProductionOptimizer.OptimizationSummary": ...

    class ConstraintDirection(
        java.lang.Enum["ProductionOptimizer.ConstraintDirection"]
    ):
        LESS_THAN: typing.ClassVar["ProductionOptimizer.ConstraintDirection"] = ...
        GREATER_THAN: typing.ClassVar["ProductionOptimizer.ConstraintDirection"] = ...
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
            string: typing.Union[java.lang.String, str]
        ) -> "ProductionOptimizer.ConstraintDirection": ...
        @staticmethod
        def values() -> (
            typing.MutableSequence["ProductionOptimizer.ConstraintDirection"]
        ): ...

    class ConstraintSeverity(java.lang.Enum["ProductionOptimizer.ConstraintSeverity"]):
        HARD: typing.ClassVar["ProductionOptimizer.ConstraintSeverity"] = ...
        SOFT: typing.ClassVar["ProductionOptimizer.ConstraintSeverity"] = ...
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
            string: typing.Union[java.lang.String, str]
        ) -> "ProductionOptimizer.ConstraintSeverity": ...
        @staticmethod
        def values() -> (
            typing.MutableSequence["ProductionOptimizer.ConstraintSeverity"]
        ): ...

    class ConstraintStatus:
        def __init__(
            self,
            string: typing.Union[java.lang.String, str],
            constraintSeverity: "ProductionOptimizer.ConstraintSeverity",
            double: float,
            double2: float,
            string2: typing.Union[java.lang.String, str],
        ): ...
        def getDescription(self) -> java.lang.String: ...
        def getMargin(self) -> float: ...
        def getName(self) -> java.lang.String: ...
        def getPenaltyWeight(self) -> float: ...
        def getSeverity(self) -> "ProductionOptimizer.ConstraintSeverity": ...
        def violated(self) -> bool: ...

    class IterationRecord:
        def __init__(
            self,
            double: float,
            string: typing.Union[java.lang.String, str],
            map: typing.Union[
                java.util.Map[typing.Union[java.lang.String, str], float],
                typing.Mapping[typing.Union[java.lang.String, str], float],
            ],
            string2: typing.Union[java.lang.String, str],
            double2: float,
            boolean: bool,
            boolean2: bool,
            boolean3: bool,
            double3: float,
            list: java.util.List["ProductionOptimizer.UtilizationRecord"],
        ): ...
        def getBottleneckName(self) -> java.lang.String: ...
        def getBottleneckUtilization(self) -> float: ...
        def getDecisionVariables(self) -> java.util.Map[java.lang.String, float]: ...
        def getRate(self) -> float: ...
        def getRateUnit(self) -> java.lang.String: ...
        def getScore(self) -> float: ...
        def getUtilizations(
            self,
        ) -> java.util.List["ProductionOptimizer.UtilizationRecord"]: ...
        def isFeasible(self) -> bool: ...
        def isHardConstraintsOk(self) -> bool: ...
        def isUtilizationWithinLimits(self) -> bool: ...

    class ManipulatedVariable:
        def __init__(
            self,
            string: typing.Union[java.lang.String, str],
            double: float,
            double2: float,
            string2: typing.Union[java.lang.String, str],
            biConsumer: typing.Union[
                java.util.function.BiConsumer[
                    jneqsim.process.processmodel.ProcessSystem, float
                ],
                typing.Callable[
                    [jneqsim.process.processmodel.ProcessSystem, float], None
                ],
            ],
        ): ...
        def apply(
            self,
            processSystem: jneqsim.process.processmodel.ProcessSystem,
            double: float,
        ) -> None: ...
        def getLowerBound(self) -> float: ...
        def getName(self) -> java.lang.String: ...
        def getUnit(self) -> java.lang.String: ...
        def getUpperBound(self) -> float: ...

    class ObjectiveType(java.lang.Enum["ProductionOptimizer.ObjectiveType"]):
        MAXIMIZE: typing.ClassVar["ProductionOptimizer.ObjectiveType"] = ...
        MINIMIZE: typing.ClassVar["ProductionOptimizer.ObjectiveType"] = ...
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
            string: typing.Union[java.lang.String, str]
        ) -> "ProductionOptimizer.ObjectiveType": ...
        @staticmethod
        def values() -> typing.MutableSequence["ProductionOptimizer.ObjectiveType"]: ...

    class OptimizationConfig:
        def __init__(self, double: float, double2: float): ...
        def capacityPercentile(
            self, double: float
        ) -> "ProductionOptimizer.OptimizationConfig": ...
        def capacityRangeForName(
            self,
            string: typing.Union[java.lang.String, str],
            capacityRange: "ProductionOptimizer.CapacityRange",
        ) -> "ProductionOptimizer.OptimizationConfig": ...
        def capacityRangeForType(
            self,
            class_: typing.Type[typing.Any],
            capacityRange: "ProductionOptimizer.CapacityRange",
        ) -> "ProductionOptimizer.OptimizationConfig": ...
        def capacityRangeSpreadFraction(
            self, double: float
        ) -> "ProductionOptimizer.OptimizationConfig": ...
        def capacityRuleForName(
            self,
            string: typing.Union[java.lang.String, str],
            capacityRule: "ProductionOptimizer.CapacityRule",
        ) -> "ProductionOptimizer.OptimizationConfig": ...
        def capacityRuleForType(
            self,
            class_: typing.Type[typing.Any],
            capacityRule: "ProductionOptimizer.CapacityRule",
        ) -> "ProductionOptimizer.OptimizationConfig": ...
        def capacityUncertaintyFraction(
            self, double: float
        ) -> "ProductionOptimizer.OptimizationConfig": ...
        def cognitiveWeight(
            self, double: float
        ) -> "ProductionOptimizer.OptimizationConfig": ...
        def columnFsFactorLimit(
            self, double: float
        ) -> "ProductionOptimizer.OptimizationConfig": ...
        def defaultUtilizationLimit(
            self, double: float
        ) -> "ProductionOptimizer.OptimizationConfig": ...
        def enableCaching(
            self, boolean: bool
        ) -> "ProductionOptimizer.OptimizationConfig": ...
        def equipmentConstraintRule(
            self, equipmentConstraintRule: "ProductionOptimizer.EquipmentConstraintRule"
        ) -> "ProductionOptimizer.OptimizationConfig": ...
        def getCapacityPercentile(self) -> float: ...
        def getCapacityRangeSpreadFraction(self) -> float: ...
        def getCapacityUncertaintyFraction(self) -> float: ...
        def getCognitiveWeight(self) -> float: ...
        def getColumnFsFactorLimit(self) -> float: ...
        def getInertiaWeight(self) -> float: ...
        def getMaxIterations(self) -> int: ...
        def getSocialWeight(self) -> float: ...
        def getSwarmSize(self) -> int: ...
        def getUtilizationMarginFraction(self) -> float: ...
        def inertiaWeight(
            self, double: float
        ) -> "ProductionOptimizer.OptimizationConfig": ...
        def maxIterations(
            self, int: int
        ) -> "ProductionOptimizer.OptimizationConfig": ...
        def rateUnit(
            self, string: typing.Union[java.lang.String, str]
        ) -> "ProductionOptimizer.OptimizationConfig": ...
        def searchMode(
            self, searchMode: "ProductionOptimizer.SearchMode"
        ) -> "ProductionOptimizer.OptimizationConfig": ...
        def socialWeight(
            self, double: float
        ) -> "ProductionOptimizer.OptimizationConfig": ...
        def swarmSize(self, int: int) -> "ProductionOptimizer.OptimizationConfig": ...
        def tolerance(
            self, double: float
        ) -> "ProductionOptimizer.OptimizationConfig": ...
        def utilizationLimitForName(
            self, string: typing.Union[java.lang.String, str], double: float
        ) -> "ProductionOptimizer.OptimizationConfig": ...
        def utilizationLimitForType(
            self, class_: typing.Type[typing.Any], double: float
        ) -> "ProductionOptimizer.OptimizationConfig": ...
        def utilizationMarginFraction(
            self, double: float
        ) -> "ProductionOptimizer.OptimizationConfig": ...

    class OptimizationConstraint:
        def __init__(
            self,
            string: typing.Union[java.lang.String, str],
            toDoubleFunction: typing.Union[
                java.util.function.ToDoubleFunction[
                    jneqsim.process.processmodel.ProcessSystem
                ],
                typing.Callable[[jneqsim.process.processmodel.ProcessSystem], float],
            ],
            double: float,
            constraintDirection: "ProductionOptimizer.ConstraintDirection",
            constraintSeverity: "ProductionOptimizer.ConstraintSeverity",
            double2: float,
            string2: typing.Union[java.lang.String, str],
        ): ...
        def getDescription(self) -> java.lang.String: ...
        def getName(self) -> java.lang.String: ...
        def getPenaltyWeight(self) -> float: ...
        def getSeverity(self) -> "ProductionOptimizer.ConstraintSeverity": ...
        @staticmethod
        def greaterThan(
            string: typing.Union[java.lang.String, str],
            toDoubleFunction: typing.Union[
                java.util.function.ToDoubleFunction[
                    jneqsim.process.processmodel.ProcessSystem
                ],
                typing.Callable[[jneqsim.process.processmodel.ProcessSystem], float],
            ],
            double: float,
            constraintSeverity: "ProductionOptimizer.ConstraintSeverity",
            double2: float,
            string2: typing.Union[java.lang.String, str],
        ) -> "ProductionOptimizer.OptimizationConstraint": ...
        def isSatisfied(
            self, processSystem: jneqsim.process.processmodel.ProcessSystem
        ) -> bool: ...
        @staticmethod
        def lessThan(
            string: typing.Union[java.lang.String, str],
            toDoubleFunction: typing.Union[
                java.util.function.ToDoubleFunction[
                    jneqsim.process.processmodel.ProcessSystem
                ],
                typing.Callable[[jneqsim.process.processmodel.ProcessSystem], float],
            ],
            double: float,
            constraintSeverity: "ProductionOptimizer.ConstraintSeverity",
            double2: float,
            string2: typing.Union[java.lang.String, str],
        ) -> "ProductionOptimizer.OptimizationConstraint": ...
        def margin(
            self, processSystem: jneqsim.process.processmodel.ProcessSystem
        ) -> float: ...

    class OptimizationObjective:
        @typing.overload
        def __init__(
            self,
            string: typing.Union[java.lang.String, str],
            toDoubleFunction: typing.Union[
                java.util.function.ToDoubleFunction[
                    jneqsim.process.processmodel.ProcessSystem
                ],
                typing.Callable[[jneqsim.process.processmodel.ProcessSystem], float],
            ],
            double: float,
        ): ...
        @typing.overload
        def __init__(
            self,
            string: typing.Union[java.lang.String, str],
            toDoubleFunction: typing.Union[
                java.util.function.ToDoubleFunction[
                    jneqsim.process.processmodel.ProcessSystem
                ],
                typing.Callable[[jneqsim.process.processmodel.ProcessSystem], float],
            ],
            double: float,
            objectiveType: "ProductionOptimizer.ObjectiveType",
        ): ...
        def evaluate(
            self, processSystem: jneqsim.process.processmodel.ProcessSystem
        ) -> float: ...
        def getName(self) -> java.lang.String: ...
        def getType(self) -> "ProductionOptimizer.ObjectiveType": ...
        def getWeight(self) -> float: ...

    class OptimizationResult:
        def __init__(
            self,
            double: float,
            string: typing.Union[java.lang.String, str],
            map: typing.Union[
                java.util.Map[typing.Union[java.lang.String, str], float],
                typing.Mapping[typing.Union[java.lang.String, str], float],
            ],
            processEquipmentInterface: jneqsim.process.equipment.ProcessEquipmentInterface,
            double2: float,
            list: java.util.List["ProductionOptimizer.UtilizationRecord"],
            map2: typing.Union[
                java.util.Map[typing.Union[java.lang.String, str], float],
                typing.Mapping[typing.Union[java.lang.String, str], float],
            ],
            list2: java.util.List["ProductionOptimizer.ConstraintStatus"],
            boolean: bool,
            double3: float,
            int: int,
            list3: java.util.List["ProductionOptimizer.IterationRecord"],
        ): ...
        def getBottleneck(
            self,
        ) -> jneqsim.process.equipment.ProcessEquipmentInterface: ...
        def getBottleneckUtilization(self) -> float: ...
        def getConstraintStatuses(
            self,
        ) -> java.util.List["ProductionOptimizer.ConstraintStatus"]: ...
        def getDecisionVariables(self) -> java.util.Map[java.lang.String, float]: ...
        def getIterationHistory(
            self,
        ) -> java.util.List["ProductionOptimizer.IterationRecord"]: ...
        def getIterations(self) -> int: ...
        def getObjectiveValues(self) -> java.util.Map[java.lang.String, float]: ...
        def getOptimalRate(self) -> float: ...
        def getRateUnit(self) -> java.lang.String: ...
        def getScore(self) -> float: ...
        def getUtilizationRecords(
            self,
        ) -> java.util.List["ProductionOptimizer.UtilizationRecord"]: ...
        def isFeasible(self) -> bool: ...

    class OptimizationSummary:
        def __init__(
            self,
            double: float,
            string: typing.Union[java.lang.String, str],
            string2: typing.Union[java.lang.String, str],
            double2: float,
            double3: float,
            double4: float,
            boolean: bool,
            map: typing.Union[
                java.util.Map[typing.Union[java.lang.String, str], float],
                typing.Mapping[typing.Union[java.lang.String, str], float],
            ],
            list: java.util.List["ProductionOptimizer.UtilizationRecord"],
            list2: java.util.List["ProductionOptimizer.ConstraintStatus"],
        ): ...
        def getConstraints(
            self,
        ) -> java.util.List["ProductionOptimizer.ConstraintStatus"]: ...
        def getDecisionVariables(self) -> java.util.Map[java.lang.String, float]: ...
        def getLimitingEquipment(self) -> java.lang.String: ...
        def getMaxRate(self) -> float: ...
        def getRateUnit(self) -> java.lang.String: ...
        def getUtilization(self) -> float: ...
        def getUtilizationLimit(self) -> float: ...
        def getUtilizationMargin(self) -> float: ...
        def getUtilizations(
            self,
        ) -> java.util.List["ProductionOptimizer.UtilizationRecord"]: ...
        def isFeasible(self) -> bool: ...

    class ScenarioComparisonResult:
        def __init__(
            self,
            string: typing.Union[java.lang.String, str],
            list: java.util.List["ProductionOptimizer.ScenarioResult"],
            map: typing.Union[
                java.util.Map[
                    typing.Union[java.lang.String, str],
                    typing.Union[
                        java.util.Map[typing.Union[java.lang.String, str], float],
                        typing.Mapping[typing.Union[java.lang.String, str], float],
                    ],
                ],
                typing.Mapping[
                    typing.Union[java.lang.String, str],
                    typing.Union[
                        java.util.Map[typing.Union[java.lang.String, str], float],
                        typing.Mapping[typing.Union[java.lang.String, str], float],
                    ],
                ],
            ],
            map2: typing.Union[
                java.util.Map[
                    typing.Union[java.lang.String, str],
                    typing.Union[
                        java.util.Map[typing.Union[java.lang.String, str], float],
                        typing.Mapping[typing.Union[java.lang.String, str], float],
                    ],
                ],
                typing.Mapping[
                    typing.Union[java.lang.String, str],
                    typing.Union[
                        java.util.Map[typing.Union[java.lang.String, str], float],
                        typing.Mapping[typing.Union[java.lang.String, str], float],
                    ],
                ],
            ],
        ): ...
        def getBaselineScenario(self) -> java.lang.String: ...
        def getKpiDeltas(
            self,
        ) -> java.util.Map[
            java.lang.String, java.util.Map[java.lang.String, float]
        ]: ...
        def getKpiValues(
            self,
        ) -> java.util.Map[
            java.lang.String, java.util.Map[java.lang.String, float]
        ]: ...
        def getScenarioResults(
            self,
        ) -> java.util.List["ProductionOptimizer.ScenarioResult"]: ...

    class ScenarioKpi:
        def __init__(
            self,
            string: typing.Union[java.lang.String, str],
            string2: typing.Union[java.lang.String, str],
            toDoubleFunction: typing.Union[
                java.util.function.ToDoubleFunction[
                    "ProductionOptimizer.OptimizationResult"
                ],
                typing.Callable[["ProductionOptimizer.OptimizationResult"], float],
            ],
        ): ...
        def evaluate(
            self, optimizationResult: "ProductionOptimizer.OptimizationResult"
        ) -> float: ...
        def getName(self) -> java.lang.String: ...
        def getUnit(self) -> java.lang.String: ...
        @staticmethod
        def objectiveValue(
            string: typing.Union[java.lang.String, str]
        ) -> "ProductionOptimizer.ScenarioKpi": ...
        @staticmethod
        def optimalRate(
            string: typing.Union[java.lang.String, str]
        ) -> "ProductionOptimizer.ScenarioKpi": ...
        @staticmethod
        def score() -> "ProductionOptimizer.ScenarioKpi": ...

    class ScenarioRequest:
        @typing.overload
        def __init__(
            self,
            string: typing.Union[java.lang.String, str],
            processSystem: jneqsim.process.processmodel.ProcessSystem,
            list: java.util.List["ProductionOptimizer.ManipulatedVariable"],
            optimizationConfig: "ProductionOptimizer.OptimizationConfig",
            list2: java.util.List["ProductionOptimizer.OptimizationObjective"],
            list3: java.util.List["ProductionOptimizer.OptimizationConstraint"],
        ): ...
        @typing.overload
        def __init__(
            self,
            string: typing.Union[java.lang.String, str],
            processSystem: jneqsim.process.processmodel.ProcessSystem,
            streamInterface: jneqsim.process.equipment.stream.StreamInterface,
            optimizationConfig: "ProductionOptimizer.OptimizationConfig",
            list: java.util.List["ProductionOptimizer.OptimizationObjective"],
            list2: java.util.List["ProductionOptimizer.OptimizationConstraint"],
        ): ...
        def getConfig(self) -> "ProductionOptimizer.OptimizationConfig": ...
        def getConstraints(
            self,
        ) -> java.util.List["ProductionOptimizer.OptimizationConstraint"]: ...
        def getFeedStream(self) -> jneqsim.process.equipment.stream.StreamInterface: ...
        def getName(self) -> java.lang.String: ...
        def getObjectives(
            self,
        ) -> java.util.List["ProductionOptimizer.OptimizationObjective"]: ...
        def getProcess(self) -> jneqsim.process.processmodel.ProcessSystem: ...
        def getVariables(
            self,
        ) -> java.util.List["ProductionOptimizer.ManipulatedVariable"]: ...

    class ScenarioResult:
        def __init__(
            self,
            string: typing.Union[java.lang.String, str],
            optimizationResult: "ProductionOptimizer.OptimizationResult",
        ): ...
        def getName(self) -> java.lang.String: ...
        def getResult(self) -> "ProductionOptimizer.OptimizationResult": ...

    class SearchMode(java.lang.Enum["ProductionOptimizer.SearchMode"]):
        BINARY_FEASIBILITY: typing.ClassVar["ProductionOptimizer.SearchMode"] = ...
        GOLDEN_SECTION_SCORE: typing.ClassVar["ProductionOptimizer.SearchMode"] = ...
        NELDER_MEAD_SCORE: typing.ClassVar["ProductionOptimizer.SearchMode"] = ...
        PARTICLE_SWARM_SCORE: typing.ClassVar["ProductionOptimizer.SearchMode"] = ...
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
            string: typing.Union[java.lang.String, str]
        ) -> "ProductionOptimizer.SearchMode": ...
        @staticmethod
        def values() -> typing.MutableSequence["ProductionOptimizer.SearchMode"]: ...

    class UtilizationRecord:
        def __init__(
            self,
            string: typing.Union[java.lang.String, str],
            double: float,
            double2: float,
            double3: float,
            double4: float,
        ): ...
        def getCapacityDuty(self) -> float: ...
        def getCapacityMax(self) -> float: ...
        def getEquipmentName(self) -> java.lang.String: ...
        def getUtilization(self) -> float: ...
        def getUtilizationLimit(self) -> float: ...

    class UtilizationSeries:
        def __init__(
            self,
            string: typing.Union[java.lang.String, str],
            list: java.util.List[float],
            list2: java.util.List[bool],
            double: float,
        ): ...
        def getBottleneckFlags(self) -> java.util.List[bool]: ...
        def getEquipmentName(self) -> java.lang.String: ...
        def getUtilizationLimit(self) -> float: ...
        def getUtilizations(self) -> java.util.List[float]: ...

    class CapacityRange: ...
    class CapacityRule: ...
    class EquipmentConstraintRule: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.util.optimization")``.

    BatchStudy: typing.Type[BatchStudy]
    ProductionOptimizationSpecLoader: typing.Type[ProductionOptimizationSpecLoader]
    ProductionOptimizer: typing.Type[ProductionOptimizer]
