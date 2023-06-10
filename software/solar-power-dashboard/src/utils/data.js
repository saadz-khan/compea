import { onValue, ref, limitToLast, query, set, child } from "firebase/database";
import { InitializeFirebase } from "./firebase";
import {
  CONTROL_CONNECTION_DETAILS,
  POWER_CONNECTION_DETAILS,
  WEATHER_CONNECTION_DETAILS,
  FORECAST_CONNECTION_DETAILS
} from "./config";

export const getData = async () => {
  return new Promise((resolve, reject) => {
    const db = InitializeFirebase(WEATHER_CONNECTION_DETAILS, "app1");
    const dbRef = query(ref(db), limitToLast(1000));

    onValue(dbRef, (snapshot) => {
      let dummyData = [];
      snapshot.forEach((child) => {
        let childData = child.val();
        dummyData.push(childData);
      });
      resolve(dummyData.reverse());
    });
  });
};

export const getPowerData = async () => {
  return new Promise((resolve, reject) => {
    const db = InitializeFirebase(POWER_CONNECTION_DETAILS, "app2");
    const dbRef = query(ref(db), limitToLast(400));

    onValue(dbRef, (snapshot) => {
      let dummyData = [];
      snapshot.forEach((child) => {
        let childData = child.val();
        dummyData.push(childData);
      });
      resolve(dummyData.reverse());
    });
  });
};

export const getControlsData = async () => {
  return new Promise((resolve, reject) => {
    const db = InitializeFirebase(CONTROL_CONNECTION_DETAILS);
    const dbRef = ref(db);

    onValue(dbRef, (snapshot) => {
      resolve(snapshot.val());
    });
  });
};

export const pushControlsData = async (newData) => {
  return new Promise((resolve, reject) => {
    const db = InitializeFirebase(CONTROL_CONNECTION_DETAILS);
    const dbRef = ref(db);
    set(dbRef, newData).then(resolve, reject);
  });
};

export const getForecastData = async () => {
  return new Promise((resolve, reject) => {
    const db = InitializeFirebase(FORECAST_CONNECTION_DETAILS, "app3");
    const dbRef = query(ref(db), limitToLast(700));

    onValue(dbRef, (snapshot) => {
      let forecastData = [];
      snapshot.forEach((child) => {
        let childData = child.val();
        forecastData.push(childData);
      });
      resolve(forecastData.reverse());
    });
  });
};


export const getConsumptionData = async () => {
  return new Promise((resolve, reject) => {
    const db = InitializeFirebase(FORECAST_CONNECTION_DETAILS, "app3");
    const dbRef = child(ref(db), "consumption", limitToLast(300)); // Fetch data from the "/consumption" child node

    onValue(dbRef, (snapshot) => {
      let consumptionData = [];
      snapshot.forEach((child) => {
        let childData = child.val();
        consumptionData.push(childData);
      });
      resolve(consumptionData.reverse());
    });
  });
};


