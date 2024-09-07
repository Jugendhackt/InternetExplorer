import { HistoryEntry } from "./HistoryEntry";
import PageArea from "./PageArea";
import PromptBox from "./PromptBox";

interface Props {
  historyEntries: HistoryEntry[];
}

const History = ({ historyEntries }: Props) => {
  // TODO make this column twice the width
  return (
    <PageArea className="flex-grow-2" title="Conversation">
      {historyEntries.map((entry) => {
        return entry.render();
      })}

      <PromptBox />
    </PageArea>
  );
};

export default History;
