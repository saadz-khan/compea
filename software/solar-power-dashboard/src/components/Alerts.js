import { Box } from "@material-ui/core";
import { Alert } from "@material-ui/lab";
import { useMemo } from "react";

const getPriority = (recString) => {
  if (recString.toLowerCase().match(/(high|highest)/)) {
    return "error";
  } else if (recString.toLowerCase().match(/low/)) {
    return "info";
  } else return "warning";
};

export const Alerts = (props) => {
  const { latestControlsData } = props;

  const recommendations = useMemo(() => {
    if (!latestControlsData.Recommendations) return [];
    const recStrings = latestControlsData.Recommendations.split(".");
    recStrings.pop();
    return recStrings.map((recString) => ({
      text: recString,
      severity: getPriority(recString),
    }));
  }, [latestControlsData]);

  return (
    <>
      {recommendations.map((recommendation) => (
        <Box margin={1}>
          <Alert severity={recommendation.severity}>
            {recommendation.text}
          </Alert>
        </Box>
      ))}
    </>
  );
};
