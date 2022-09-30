from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ViewConfig:
    v_name: str
    v_id: str


@dataclass(frozen=True)
class WorkbookConfig:
    wb_name: str
    wb_id: str
    views: List[ViewConfig]


workbook_config = [
    WorkbookConfig(wb_name="Proprietary Traffic Dashboards",
                   wb_id="97239f76-6325-4d0c-9a76-3500a756b577",
                   views=[ViewConfig(v_name="Proprietary Brand Dashboard",
                                     v_id='d9e5e3a9-926e-4d21-8ae3-526496bb364f'),
                          ViewConfig(v_name="Proprietary Asset & OS Dashboard",
                                     v_id='ec57a4b2-465b-4906-95c6-26dae09cc53c')]
                   ),
    WorkbookConfig(wb_name="Data Review Dashboards",
                   wb_id="533dbfb7-45b3-4dea-93aa-59db50e250f6",
                   views=[ViewConfig(v_name="Data Publication Preview",
                                     v_id='e383eefc-6340-4ede-b4c4-fa87c89dc5c0'),
                          ViewConfig(v_name="View for Data Review",
                                     v_id='2af16571-351c-48cc-a2a2-fd4339a506f8')]
                   )
]
