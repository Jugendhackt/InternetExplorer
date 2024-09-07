import ActionDetailEntry from "./ActionDetailEntry";
import PageArea from "./PageArea";

interface Props {
  data: Map<string, string>;
}

const ActionDetails = ({data}: Props) => { 

  if (typeof(data) == "object") {
    data = new Map(Object.entries(data));
  }
  
  return (
    <PageArea title="Action Details" className="rounded-end">
      {Array.from(data.entries()).map(([key, value]) => (
        <ActionDetailEntry key={key} detailKey={key} detailValue={value} />
      ))}
    </PageArea>
  );
};

export default ActionDetails;
