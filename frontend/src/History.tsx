import BrowseActionEntryComponent, {
  BrowseActionEntry,
} from "./data/BrowseActionEntry";
import { HistoryEntry } from "./data/HistoryEntry";
import PageArea from "./PageArea";
import PromptBox from "./PromptBox";
import { WebsocketSender } from "./util/WebsocketUtil";

interface Props {
  historyEntries: HistoryEntry[];
  setActionDetails: (actionDetails: Map<string, string>) => void;
  sendMessage: WebsocketSender;
}

const History = ({ historyEntries, setActionDetails, sendMessage }: Props) => {
  // TODO make this column twice the width
  return (
    <PageArea className="flex-grow-2" title="Conversation">
      {historyEntries.map((entry) => {
        if (entry instanceof BrowseActionEntry) {
          return (
            <BrowseActionEntryComponent
              browseActionEntry={entry}
              setActionDetails={setActionDetails}
            />
          );
        }
        return entry.render();
      })}

      <PromptBox sendMessage={sendMessage} />
    </PageArea>
  );
};

export default History;
