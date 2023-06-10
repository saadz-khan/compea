import { ResponsiveLine } from "@nivo/line";
import { useMemo, useState } from "react";
import { Buttons } from "./Buttons";

const CHART_SIZE = 80;

export const ConsumptionChart = (props) => {
  const { consumptionData } = props;
  const [offset, setOffset] = useState(0);

  const chartData = useMemo(() => {
    const slicedConsumptionData = consumptionData.slice(offset, offset + CHART_SIZE);
    return [
      {
        id: "Active Power",
        data: slicedConsumptionData.map((item) => ({
          x: item.DATE_TIME, // Convert DATE_TIME to Date type
          y: item.Global_active_power
        })),
      },
    ];
  }, [consumptionData, offset]);

  const handleChartBack = () => {
    if (offset < consumptionData.length - CHART_SIZE) {
      setOffset(offset + 10);
    } else {
      setOffset(consumptionData.length - CHART_SIZE);
    }
  };
  const handleChartForward = () => {
    if (offset > 0 && offset >= CHART_SIZE) {
      setOffset(offset - CHART_SIZE);
    } else if (offset > 0) {
      setOffset(0);
    }
  };

  if (!consumptionData) {
    return <div>Loading forecast data...</div>;
  }

  return (
    <div>
      <div style={{ height: 400 }}>
        <ResponsiveLine
          data={chartData}
          margin={{ top: 50, right: 110, bottom: 50, left: 60 }}
          xScale={{
            type: "time",
            format: "%Y-%m-%d",
          }}
          xFormat="time:%Y-%m-%d"
          yScale={{
            type: "linear",
            stacked: false,
            reverse: false,
            min: 0,
            max: 2700,
          }}
          axisTop={null}
          axisRight={null}
          axisBottom={{
            tickSize: 2,
            tickPadding: 5,
            tickRotation: 0,
            legend: "Time",
            format: "%Y-%m-%d",
            legendOffset: 36,
            legendPosition: "middle",
          }}
          axisLeft={{
            tickSize: 5,
            tickPadding: 5,
            tickRotation: 0,
            legend: "Active Power",
            legendOffset: -40,
            legendPosition: "middle",
          }}
          pointSize={10}
          pointColor={{ theme: "background" }}
          pointBorderWidth={2}
          pointBorderColor={{ from: "serieColor" }}
          pointLabelYOffset={-12}
          useMesh={true}
          legends={[
            {
              anchor: "bottom-right",
              direction: "column",
              justify: false,
              translateX: 100,
              translateY: 0,
              itemsSpacing: 0,
              itemDirection: "left-to-right",
              itemWidth: 80,
              itemHeight: 20,
              itemOpacity: 0.75,
              symbolSize: 12,
              symbolShape: "circle",
              symbolBorderColor: "rgba(0, 0, 0, .5)",
              effects: [
                {
                  on: "hover",
                  style: {
                    itemBackground: "rgba(0, 0, 0, .03)",
                    itemOpacity: 1,
                  },
                },
              ],
            },
          ]}
        />
      </div>
      <Buttons onNext={handleChartForward} onBack={handleChartBack} />
    </div>
  );
};

      
export default ConsumptionChart;
