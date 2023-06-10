import moment from "moment";

export const jitter = (item, index) => {
  const date = moment(item.x, "MM/DD/YYYY HH:mm");
  date.add(index * 5, "seconds");
  const formattedDate = date.format("MM/DD/YYYY HH:mm:ss");
  return {
    ...item,
    x: formattedDate,
  };
};
