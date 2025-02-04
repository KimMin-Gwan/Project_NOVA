import { create } from "zustand";

const useLoginStore = create((set) => ({
  isLogin: "",
  isLogout: false,

  tryLogout: () => set({ isLogin: "" }),
  tryLogin: (status) => set({ isLogin: status }),
}));

export default useLoginStore;
