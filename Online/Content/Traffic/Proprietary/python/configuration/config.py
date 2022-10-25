from dataclasses import dataclass
from datetime import date
from typing import List


@dataclass(frozen=True)
class ViewConfig:
    v_name: str
    v_id: str
    date_chunks: bool


@dataclass(frozen=True)
class WorkbookConfig:
    wb_name: str
    wb_id: str
    views: List[ViewConfig]

START_DATE = date(year=2022, month=4, day=1)

workbook_config = [
    WorkbookConfig(wb_name="ProprietaryAPITrafficDashboards",
                   wb_id="79119cc9-7a49-4117-9c3e-84b385e307be",
                   views=[ViewConfig(v_name="Brand Total Daily",
                                     v_id='c4a00b70-f0e1-4d5f-bbfb-fcb782916652',
                                     date_chunks=False),
                          ViewConfig(v_name="Brand Devices Daily",
                                     v_id='c6c0dfe6-4b48-4296-8592-e75bd522975c',
                                     date_chunks=True),
                          ViewConfig(v_name="Asset & OS Total Daily",
                                     v_id='aac0ec16-6258-4578-acf7-cf75eb8587df',
                                     date_chunks=True),
                          ViewConfig(v_name="Asset & OS Devices Daily",
                                     v_id='4b98556e-ae1a-42ca-aa29-24fbb9792c48',
                                     date_chunks=True)
                          ])
]