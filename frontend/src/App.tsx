import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.bundle.min";
import { UserInputEntry } from "./data/UserInputEntry";
import { BrowseAction, BrowseActionEntry } from "./data/BrowseActionEntry";
import { useEffect, useState } from "react";
import useWebSocket from "react-use-websocket";
import Settings from "./Settings";
import History from "./History";
import ActionDetails from "./ActionDetails";
import { HistoryEntry } from "./data/HistoryEntry";
import ConnectionStatus from "./ConnectionStatus";

function App() {
  const [actionDetails, setActionDetails] = useState(
    new Map([["test key", "test value"]])
  );

  const [historyEntries, setHistoryEntries] = useState<HistoryEntry[]>([]);

  const { sendMessage, lastMessage, readyState } = useWebSocket(
    "ws://127.0.0.1:1000"
  );

  useEffect(() => {
    if (lastMessage !== null) {
      console.log(lastMessage.data);
      const data = JSON.parse(lastMessage.data);
      const action = data["action"];
      switch (action) {
        case "input":
          const inputType = data["inputType"];
          const inputText = data["inputText"];
          const historyEntry = new UserInputEntry(inputType, inputText);
          setHistoryEntries([...historyEntries, historyEntry]);
          return;
        case "action_entry":
          const actions = data["actions"];
          const parsedActionsList: BrowseAction[] = [];
          actions.forEach((action: any) => {
            const type = action["type"];
            const actionData = action["actionData"];
            const result = action["result"];

            parsedActionsList.push(new BrowseAction(type, actionData, result));
          });

          const browseActionEntry = new BrowseActionEntry(parsedActionsList);
          setHistoryEntries([...historyEntries, browseActionEntry]);
          return;
      }
    }
  }, [lastMessage]);

  return (
    <div>
      <h1 className="text-center">✨ Internet Explorer
        <ConnectionStatus readyState={readyState}/>
      </h1>
      <div className="d-flex flex-row align-items-stretch justify-content-evenly m-2 main-layout">
        <Settings sendMessage={sendMessage} />
        <History
          historyEntries={historyEntries}
          setActionDetails={setActionDetails}
          sendMessage={sendMessage}
        />
        <ActionDetails data={actionDetails} />
      </div>
    </div>
  );
}

export default App;
