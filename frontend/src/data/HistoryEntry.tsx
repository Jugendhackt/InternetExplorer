import { ReactNode } from "react";

export abstract class HistoryEntry {
  abstract render(): ReactNode;
}
