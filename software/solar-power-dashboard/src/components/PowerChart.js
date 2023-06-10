import { ResponsivePie } from "@nivo/pie";
import { useMemo } from "react";

export const PowerChart = (props) => {
  const { powerData } = props;

  const pieChartData = useMemo(() => {
    const acPower = powerData[0]?.AC_POWER ?? 0;
    const dcPower = powerData[0]?.DC_POWER ?? 0;
    const totalPower = acPower + dcPower;

    if (totalPower === 0) {
      return [
        {
          id: "No Power",
          label: "No Power",
          value: 100,
        },
      ];
    }

    return [
      {
        id: "AC Power",
        label: "AC Power",
        value: parseFloat(((acPower / totalPower) * 100).toFixed(2)),
      },
      {
        id: "DC Power",
        label: "DC Power",
        value: parseFloat(((dcPower / totalPower) * 100).toFixed(2)),
      },
    ];
  }, [powerData]);

  return (
    <div style={{ height: 400 }}>
      <ResponsivePie
        data={pieChartData}
        colors={["#06AFFE", "#7605FF"]}
        margin={{ top: 40, right: 80, bottom: 80, left: 80 }}
        innerRadius={0.5}
        padAngle={0.7}
        cornerRadius={3}
        borderWidth={1}
        borderColor={{ from: "color", modifiers: [["darker", 0.2]] }}
        radialLabelsSkipAngle={10}
        radialLabelsTextColor="#333333"
        radialLabelsLinkColor={{ from: "color" }}
        sliceLabelsSkipAngle={10}
        sliceLabelsTextColor="#333333"
        legends={[
          {
            anchor: "bottom",
            direction: "row",
            justify: false,
            translateX: 0,
            translateY: 56,
            itemsSpacing: 0,
            itemWidth: 100,
            itemHeight: 18,
            itemTextColor: "#999",
            itemDirection: "left-to-right",
            itemOpacity: 1,
            symbolSize: 18,
            symbolShape: "circle",
            effects: [
              {
                on: "hover",
                style: {
                  itemTextColor: "#000",
                  itemOpacity: 1,
                },
              },
            ],
          },
        ]}
      />
    </div>
  );
};
