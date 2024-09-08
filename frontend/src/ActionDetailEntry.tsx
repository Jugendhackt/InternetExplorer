import Linkify from "linkify-react";

interface Props {
  detailKey: string;
  detailValue: string;
}

const ActionDetailEntry = ({ detailKey, detailValue }: Props) => {
  return (
    <p className="d-flex justify-content-between">
      <span className="text-start">{detailKey}:</span>
      <span className="text-end">
        <Linkify>{detailValue}</Linkify>
      </span>
    </p>
  );
};

export default ActionDetailEntry;
