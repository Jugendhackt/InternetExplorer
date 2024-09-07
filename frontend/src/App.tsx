import "bootstrap/dist/css/bootstrap.css";
import Settings from "./Settings";
import History from "./History";
import ActionDetails from "./ActionDetails";
import { HistoryEntry, UserInputEntry } from "./HistoryEntry";

const historyEntries: HistoryEntry[] = [
  new UserInputEntry("voice", "Geh auf YouTube und suche nach Fortnite."),
];

function App() {
  return (
    <>
      <div>
        <h1 className="text-center">Internet Explorer</h1>
        <div className="d-flex flex-row align-items-stretch justify-content-evenly m-2">
          <Settings />
          <History historyEntries={historyEntries} />
          <ActionDetails />
        </div>
      </div>
    </>
  );
}

export default App;
