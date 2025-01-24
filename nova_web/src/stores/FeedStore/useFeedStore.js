import axios from "axios";
import { create } from "zustand";
import getTagList from "../../services/getTagList";
const useFeedStore = create((set) => ({
  feedList: [],
  loading: false,
  error: null,

  //   getFeedList: async () => {
  //     set({ loading: true, error: null });
  //     try{
  //         const res = await
  //     }
  //   },

  //   fetchTagList: async () => {
  //     set({ loading: true, error: null });
  //     try {
  //       const res = await getTagList();
  //       set({ tagList: res.body.hashtags, loading: false });
  //     } catch (err) {
  //       set({ error: err.message, loading: false });
  //     }
  //   },
}));

export default useFeedStore;
