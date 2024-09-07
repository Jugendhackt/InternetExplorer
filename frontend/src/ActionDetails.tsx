import ActionDetailEntry from "./ActionDetailEntry";
import PageArea from "./PageArea";

const ActionDetails = () => {
  return (
    <PageArea title="Action Details" className="rounded-end">
      <ActionDetailEntry detailKey="Type" detailValue="Click element"/>
    </PageArea>
  );
};

export default ActionDetails;
