import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import jpype
import typing

class AdvancedProcessLogicExample:
    def __init__(self): ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...

class BeggsAndBrillsValidationExample:
    def __init__(self): ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...

class ConfigurableLogicExample:
    def __init__(self): ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...

class DynamicLogicExample:
    def __init__(self): ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...

class ESDBlowdownSystemExample:
    def __init__(self): ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...

class ESDLogicExample:
    def __init__(self): ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...

class ESDValveExample:
    def __init__(self): ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...

class FireGasSISExample:
    def __init__(self): ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...

class FourWellManifoldWithHeatTransferAdjustmentExample:
    def __init__(self): ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...

class HIPPSExample:
    def __init__(self): ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...

class HIPPSWithESDExample:
    def __init__(self): ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...

class IntegratedSafetySystemExample:
    def __init__(self): ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...

class IntegratedSafetySystemWithLogicExample:
    def __init__(self): ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...

class ProcessLogicAlarmIntegratedExample:
    def __init__(self): ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...

class ProcessLogicIntegratedExample:
    def __init__(self): ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...

class SelectiveLogicExecutionExample:
    def __init__(self): ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...

class SeparatorFireDepressurizationExample:
    def __init__(self): ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...

class SeparatorHeatInputExample:
    def __init__(self): ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...

class TransientPipeHeatTransferExample:
    def __init__(self): ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.util.example")``.

    AdvancedProcessLogicExample: typing.Type[AdvancedProcessLogicExample]
    BeggsAndBrillsValidationExample: typing.Type[BeggsAndBrillsValidationExample]
    ConfigurableLogicExample: typing.Type[ConfigurableLogicExample]
    DynamicLogicExample: typing.Type[DynamicLogicExample]
    ESDBlowdownSystemExample: typing.Type[ESDBlowdownSystemExample]
    ESDLogicExample: typing.Type[ESDLogicExample]
    ESDValveExample: typing.Type[ESDValveExample]
    FireGasSISExample: typing.Type[FireGasSISExample]
    FourWellManifoldWithHeatTransferAdjustmentExample: typing.Type[
        FourWellManifoldWithHeatTransferAdjustmentExample
    ]
    HIPPSExample: typing.Type[HIPPSExample]
    HIPPSWithESDExample: typing.Type[HIPPSWithESDExample]
    IntegratedSafetySystemExample: typing.Type[IntegratedSafetySystemExample]
    IntegratedSafetySystemWithLogicExample: typing.Type[
        IntegratedSafetySystemWithLogicExample
    ]
    ProcessLogicAlarmIntegratedExample: typing.Type[ProcessLogicAlarmIntegratedExample]
    ProcessLogicIntegratedExample: typing.Type[ProcessLogicIntegratedExample]
    SelectiveLogicExecutionExample: typing.Type[SelectiveLogicExecutionExample]
    SeparatorFireDepressurizationExample: typing.Type[
        SeparatorFireDepressurizationExample
    ]
    SeparatorHeatInputExample: typing.Type[SeparatorHeatInputExample]
    TransientPipeHeatTransferExample: typing.Type[TransientPipeHeatTransferExample]
