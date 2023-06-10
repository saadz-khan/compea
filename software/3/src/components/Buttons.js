import { Button } from "@material-ui/core";
import { ArrowLeft, ArrowRight } from "@material-ui/icons";

export const Buttons = (props) => {
  const { onNext, onBack } = props;
  return (
    <div style={{ textAlign: "center" }}>
      <Button
        style={{ marginLeft: "5px", marginRight: "5px" }}
        variant="outlined"
        onClick={onBack}
      >
        <ArrowLeft />
      </Button>
      <Button
        style={{ marginLeft: "5px", marginRight: "5px" }}
        variant="outlined"
        onClick={onNext}
      >
        <ArrowRight />
      </Button>
    </div>
  );
};
