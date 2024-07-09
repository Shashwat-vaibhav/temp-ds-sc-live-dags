from enum import Enum, unique


@unique
class POC(Enum):
    """
    _summary_
    Here we keep a unique list all POC to make sure \
    alerting / ownership is easy to identify from code
    to the labels.
    Add a pod here if needed.
    """

    DEEKSHA_KOUL = "<@U04GY141370>"
    SHASHWAT_VAIBHAV = "<@U03N5KY1WNN>"
