import "bootstrap/dist/css/bootstrap.css";
import { HistoryEntry } from "./data/HistoryEntry";
import { UserInputEntry } from "./data/UserInputEntry";
import { BrowseAction, BrowseActionEntry } from "./data/BrowseActionEntry";
import { useCallback, useEffect, useState } from "react";
import useWebSocket, { ReadyState } from "react-use-websocket";
import Settings from "./Settings";
import History from "./History";
import ActionDetails from "./ActionDetails";

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

  const { sendMessage, lastMessage, readyState } = useWebSocket("ws://127.0.0.1:1000");

  useEffect(() => {
    if (lastMessage !== null) {
      // TODO
    }
  }, [lastMessage]);

  const connectionStatus = {
    [ReadyState.CONNECTING]: "Connecting",
    [ReadyState.OPEN]: "Open",
    [ReadyState.CLOSING]: "Closing",
    [ReadyState.CLOSED]: "Closed",
    [ReadyState.UNINSTANTIATED]: "Uninstantiated",
  }[readyState];

  return (
    <div>
      <h1 className="text-center">Internet Explorer</h1>
      <div className="d-flex flex-row align-items-stretch justify-content-evenly m-2 main-layout">
        <Settings />
        <History
          historyEntries={historyEntries}
          setActionDetails={setActionDetails}
        />
        <ActionDetails data={actionDetails} />
      </div>
    </div>
  );
}

export default App;
