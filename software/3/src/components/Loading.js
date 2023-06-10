import { Box, CircularProgress } from "@material-ui/core";

export const Loading = () => {
  return (
    <Box marginTop={6} style={{ display: "flex", justifyContent: "center" }}>
      <CircularProgress color="primary" />
    </Box>
  );
};
