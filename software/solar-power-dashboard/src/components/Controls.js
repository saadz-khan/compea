import { Box, Card, CardContent, Switch, Typography } from "@material-ui/core";
import { useMemo } from "react";

export const Controls = (props) => {
  const { data, onChangeControlsData } = props;

  const manualOverride = useMemo(() => {
    return data.ManualOverride === "1";
  }, [data]);

  const handleChangeFlag = (value, key) => {
    const newData = { ...data };
    newData[key] = value ? "1" : "0";
    onChangeControlsData(newData);
  };

  return (
    <Box margin={1} marginBottom={3}>
      <Card sx={{ minWidth: 275 }}>
        <CardContent>
          <Box sx={{ display: "flex" }}>
            <Box marginX={3}>
              <Typography>Manual Override</Typography>
              <Switch
                checked={manualOverride}
                onChange={(event) =>
                  handleChangeFlag(event.target.checked, "ManualOverride")
                }
              />
            </Box>
            <Box marginX={3}>
              <Typography>Load 1</Typography>
              <Switch
                checked={data.S1 === "1"}
                disabled={!manualOverride}
                onChange={(event) =>
                  handleChangeFlag(event.target.checked, "S1")
                }
              />
            </Box>
            <Box marginX={3}>
              <Typography>Load 2</Typography>
              <Switch
                checked={data.S2 === "1"}
                disabled={!manualOverride}
                onChange={(event) =>
                  handleChangeFlag(event.target.checked, "S2")
                }
              />
            </Box>
            <Box marginX={3}>
              <Typography>Load 3</Typography>
              <Switch
                checked={data.S3 === "1"}
                disabled={!manualOverride}
                onChange={(event) =>
                  handleChangeFlag(event.target.checked, "S3")
                }
              />
            </Box>
            <Box marginX={3}>
              <Typography>Load 4</Typography>
              <Switch
                checked={data.S4 === "1"}
                disabled={!manualOverride}
                onChange={(event) =>
                  handleChangeFlag(event.target.checked, "S4")
                }
              />
            </Box>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};
