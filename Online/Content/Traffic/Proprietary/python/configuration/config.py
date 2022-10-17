from dataclasses import dataclass

from datetime import date

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


START_DATE = date(year=2021, month=6, day=1)

workbook_config = [

    WorkbookConfig(wb_name="ProprietaryAPITrafficDashboards",
                   wb_id="79119cc9-7a49-4117-9c3e-84b385e307be",
                   views=[ViewConfig(v_name="Brand Summary Data",
                                     v_id='1ea0644b-15f7-4cf6-8a8d-f5be20de710d'),
                          ViewConfig(v_name="Brand Daily Data",
                                     v_id='67375f0e-d8b5-4ef0-a98a-b1e71d26beb7'),
                          ViewConfig(v_name="Asset and OS Summary Data",
                                     v_id='197223c7-b106-4e3e-8812-55ee0749f6fd'),
                          ViewConfig(v_name="Asset and OS Daily Data",
                                     v_id='a8c3c60d-9c05-403b-94a8-0b4c8df374ae')
                          ])
]