import { ResponsiveLine } from "@nivo/line";
import { useMemo, useState } from "react";
import { jitter } from "../utils/jitter";
import { Buttons } from "./Buttons";

const CHART_SIZE = 12;

export const DailyYieldChart = (props) => {
  const { powerData } = props;

  const [offset, setOffset] = useState(0);

  const powerChartData = useMemo(() => {
    const slicedData = powerData.slice(offset, offset + CHART_SIZE);

    const chartData = slicedData
      .map((item) => ({
        x: item.DATE_TIME,
        y: item.DAILY_YIELD,
      }))
      .map(jitter);

    return [
      {
        id: "Daily Yield",
        data: chartData,
      },
    ];
  }, [powerData, offset]);

  const handleChartBack = () => {
    if (offset < powerData.length - CHART_SIZE) {
      setOffset(offset + 10);
    } else {
      setOffset(powerData.length - CHART_SIZE);
    }
  };
  const handleChartForward = () => {
    if (offset > 0 && offset >= CHART_SIZE) {
      setOffset(offset - CHART_SIZE);
    } else if (offset > 0) {
      setOffset(0);
    }
  };

  return (
    <div>
      <div style={{ height: 400 }}>
        <ResponsiveLine
          data={powerChartData}
          colors={'#FFCD05'}
          margin={{ top: 50, right: 110, bottom: 50, left: 60 }}
          xScale={{ type: "time", format: "%m/%d/%Y %H:%M:%s" }}
          xFormat="time:%m-%d-%Y %H:%M:%s"
          yScale={{
            type: "linear",
            min: "auto",
            max: "auto",
            stacked: false,
            reverse: false,
          }}
          axisTop={null}
          axisRight={null}
          axisBottom={{
            tickSize: 5,
            tickPadding: 5,
            tickRotation: 0,
            legend: "Time",
            format: "%H:%M:%s",
            legendOffset: 36,
            legendPosition: "middle",
          }}
          axisLeft={{
            tickSize: 5,
            tickPadding: 5,
            tickRotation: 0,
            legend: "Power",
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
