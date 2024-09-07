import "bootstrap/dist/css/bootstrap.css";
import { HistoryEntry } from "./data/HistoryEntry";
import { UserInputEntry } from "./data/UserInputEntry";
import { BrowseAction, BrowseActionEntry } from "./data/BrowseActionEntry";
import { useCallback, useEffect, useState } from "react";
import useWebSocket, { ReadyState } from "react-use-websocket";

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

  const [socketUrl, setSocketUrl] = useState('ws://127.0.0.1:1000');
  const [messageHistory, setMessageHistory] = useState<MessageEvent<any>[]>([]);

  const { sendMessage, lastMessage, readyState } = useWebSocket(socketUrl);

  useEffect(() => {
    if (lastMessage !== null) {
      setMessageHistory((prev) => prev.concat(lastMessage));
    }
  }, [lastMessage]);

  const handleClickSendMessage = useCallback(() => sendMessage('Hello'), []);

  const connectionStatus = {
    [ReadyState.CONNECTING]: 'Connecting',
    [ReadyState.OPEN]: 'Open',
    [ReadyState.CLOSING]: 'Closing',
    [ReadyState.CLOSED]: 'Closed',
    [ReadyState.UNINSTANTIATED]: 'Uninstantiated',
  }[readyState];

  return (
    <div>
      <button
        onClick={handleClickSendMessage}
        disabled={readyState !== ReadyState.OPEN}
      >
        Click Me to send 'Hello'
      </button>
      <span>The WebSocket is currently {connectionStatus}</span>
      {lastMessage ? <span>Last message: {lastMessage.data}</span> : null}
      <ul>
        {messageHistory.map((message, idx) => (
          <span key={idx}>{message ? message.data : null}</span>
        ))}
      </ul>
    </div>
  );

  /*
  const socket = io("http://127.0.0.1:1000");
  socket.send("hi");

 return (
    <div>
      <h1 className="text-center">Internet Explorer</h1>
      <div className="d-flex flex-row align-items-stretch justify-content-evenly m-2 main-layout">
        <Settings />
        <History historyEntries={historyEntries} setActionDetails={setActionDetails} />
        <ActionDetails data={actionDetails} />
      </div>
    </div>
  );*/
}

export default App;
