import { create } from "zustand";

const useBoardStore = create((set) => ({
  //   biasList: [],
  //   loading: false,
  //   error: null,
  board: "자유 후기 게시판",

  setBoard: (newBoard) => set({ board: newBoard }),
}));

export default useBoardStore;
