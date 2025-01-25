import { create } from "zustand";
import getTagList from "../../services/getTagList";

const useTagStore = create((set) => ({
  tagList: [],
  loading: false,
  error: null,

  fetchTagList: async () => {
    set({ loading: true, error: null });
    try {
      const res = await getTagList();
      set({ tagList: res.body.hashtags, loading: false });
    } catch (err) {
      set({ error: err.message, loading: false });
    }
  },
}));

export default useTagStore;
