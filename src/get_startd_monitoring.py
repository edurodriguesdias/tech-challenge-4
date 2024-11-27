import datetime

from sklearn import datasets

import yfinance as yf
from evidently.metrics import ColumnDriftMetric
from evidently.metrics import ColumnSummaryMetric
from evidently.metrics import DatasetDriftMetric
from evidently.metrics import DatasetMissingValuesMetric
from evidently.report import Report
from evidently.test_preset import DataDriftTestPreset
from evidently.test_suite import TestSuite
from evidently.ui.dashboards import CounterAgg
from evidently.ui.dashboards import DashboardPanelCounter
from evidently.ui.dashboards import DashboardPanelPlot
from evidently.ui.dashboards import PanelValue
from evidently.ui.dashboards import PlotType
from evidently.ui.dashboards import ReportFilter
from evidently.ui.remote import RemoteWorkspace
from evidently.ui.workspace import Workspace
from evidently.ui.workspace import WorkspaceBase
import datetime


reference_date = f'{datetime.datetime.now().year}-01-01'  

start_date = '2018-01-01'
end_date = '2024-07-20'

df = yf.download(tickers = ['PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'ABEV3.SA'], start=start_date, end=end_date)

df = df[['Close']]

df_flat = df.stack().reset_index()

df_flat.columns = ['Date', 'Ticker', 'Price']

reference_data = df_flat[df_flat['Date'] < reference_date]
current_data = df_flat[df_flat['Date'] >= reference_date]


WORKSPACE = "workspace"

PROJECT_NAME = "Stock Prices"
PROJECT_DESCRIPTION = "Data drift of yfinance b3 data."


def create_report(i: int):

    data_drift_report = Report(
        metrics=[
            DatasetDriftMetric(),  
            DatasetMissingValuesMetric(),  

            ColumnDriftMetric(column_name="Price", stattest="ks"),
        ],
        timestamp=datetime.datetime.now() + datetime.timedelta(days=i),
    )

    data_drift_report.run(reference_data=reference_data, current_data=current_data.iloc[100 * i : 100 * (i + 1), :])
    return data_drift_report



def create_test_suite(i: int):

    data_drift_test_suite = TestSuite(
        tests=[DataDriftTestPreset()],
        timestamp=datetime.datetime.now() + datetime.timedelta(days=i),
    )

    data_drift_test_suite.run(reference_data=reference_data, current_data=current_data.iloc[100 * i : 100 * (i + 1), :])
    return data_drift_test_suite



def create_project(workspace: WorkspaceBase):
    project = workspace.create_project(PROJECT_NAME)
    project.description = PROJECT_DESCRIPTION


    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Price Column Drift",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(
                    metric_id="ColumnDriftMetric",
                    metric_args={"column_name.name": "Price"}, 
                    field_path=ColumnDriftMetric.fields.drift_score, 
                    legend="Drift Score",
                ),
            ],
            plot_type=PlotType.LINE,  
        )
    )

    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Price Drift (Bar Chart)",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(
                    metric_id="ColumnDriftMetric",
                    metric_args={"column_name.name": "Price"},
                    field_path=ColumnDriftMetric.fields.drift_score,
                    legend="Drift Score",
                ),
            ],
            plot_type=PlotType.BAR,  
        )
    )

    project.save()
    return project



def create_demo_project(workspace: str):
    ws = Workspace.create(workspace)
    project = create_project(ws)

    for i in range(0, 5):
        report = create_report(i=i)
        ws.add_report(project.id, report)

        test_suite = create_test_suite(i=i)
        ws.add_test_suite(project.id, test_suite)


if __name__ == "__main__":
    create_demo_project(WORKSPACE)