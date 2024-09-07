import React from "react";

interface PageAreaProps {
  children: React.ReactNode;
  className?: string;
  title: string;
}

const PageArea = ({ children, className, title }: PageAreaProps) => {
  return (
    <div
      className={
        "p-2 w-100 bg-body-secondary border border-dark-subtle text-center " + (className ?? "")
      }
    >
      <h2 className="fs-6 text-muted">{title}</h2>
      {children}
    </div>
  );
};

export default PageArea;
