import { ResponsiveLine } from "@nivo/line";
import { useMemo, useState } from "react";
import { Buttons } from "./Buttons";

const CHART_SIZE = 25;
export const TemperatureChart = (props) => {
  const { data } = props;
  const [offset, setOffset] = useState(0);

  const chartData = useMemo(() => {
    const slicedData = data.slice(offset, offset + CHART_SIZE);
    return [
      {
        id: "Ambient Temperature",
        //colors: "hsl(200, 80%, 50%)",
        data: slicedData.map((item, index) => ({
          x: item.DATE_TIME,
          y: item.AMBIENT_TEMPERATURE,
        })),
      },
      {
        id: "Module Temperature",
        //color: "hsl(350, 51%, 50%)",
        data: slicedData.map((item, index) => ({
          x: item.DATE_TIME,
          y: item.MODULE_TEMPERATURE,
        })),
      },
    ];
  }, [data, offset]);

  const handleChartBack = () => {
    //console.log("going back");
    if (offset < data.length - CHART_SIZE) {
      setOffset(offset + 10);
    } else {
      setOffset(data.length - CHART_SIZE);
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
        colors={['#D92629', '#F2E41C']}
          data={chartData}
          margin={{ top: 50, right: 110, bottom: 50, left: 60 }}
          xScale={{ type: "time", format: "%d/%m/%Y %H:%M" }} //05/15/2020 0:00
          xFormat="time:%d-%m-%Y %H:%M"
          yScale={{
            type: "linear",
            min: 0,
            max: 50,
            stacked: false,
            reverse: false,
          }}
          axisTop={null}
          axisRight={null}
          axisBottom={{
            tickSize: 2,
            tickPadding: 5,
            tickRotation: 0,
            legend: "Time",
            format: "%d-%m-%Y %H:%M",
            legendOffset: 36,
            legendPosition: "middle",
          }}
          axisLeft={{
            tickSize: 5,
            tickPadding: 5,
            tickRotation: 0,
            legend: "Temperature (C)",
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
