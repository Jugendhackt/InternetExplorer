import "bootstrap/dist/css/bootstrap.css";
import Settings from "./Settings";
import History from "./History";
import ActionDetails from "./ActionDetails";
import { HistoryEntry } from "./data/HistoryEntry";
import { UserInputEntry } from "./data/UserInputEntry";
import { BrowseAction, BrowseActionEntry } from "./data/BrowseActionEntry";
import { act, useState } from "react";

const historyEntries: HistoryEntry[] = [
  new UserInputEntry("voice", "Geh auf YouTube und suche nach Fortnite."),
  new BrowseActionEntry([
    new BrowseAction(
      "click_element",
      new Map([["selector", "#search_box"]]),
      "success"
    ),
  ]),
];

function App() {
  const [actionDetails, setActionDetails] = useState(
    new Map([["test key", "test value"]])
  );

  return (
    <div>
      <h1 className="text-center">Internet Explorer</h1>
      <div className="d-flex flex-row align-items-stretch justify-content-evenly m-2 main-layout">
        <Settings />
        <History historyEntries={historyEntries} setActionDetails={setActionDetails} />
        <ActionDetails data={actionDetails} />
      </div>
    </div>
  );
}

export default App;
