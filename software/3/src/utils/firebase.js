import { initializeApp } from "firebase/app";
import { getDatabase } from "firebase/database";

function InitializeFirebase(config, appName) {
  const app = initializeApp(config, appName);
  return getDatabase(app);
}

export { InitializeFirebase };
