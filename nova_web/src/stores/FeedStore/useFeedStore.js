import { create } from "zustand";
import mainApi from "../../services/apis/mainApi";

const useFeedStore = create((set) => ({
  feedDatas: [],
  nextKey: -1,
  loadings: false,
  error: null,

  fetchFeedList: async (type) => {
    set({ loadings: true, error: null, feedDatas: [] });
    try {
      const res = await mainApi.get(`feed_explore/${type}_best`);
      console.log("rererere", type, res.data);
      set({ feedDatas: res.data.body.send_data, nextKey: res.data.body.key, loadings: false });
    } catch (err) {
      set({ error: err.message, loadings: false });
    }
  },

  fetchMoreFeedList: async (type, nextData) => {
    set({ loadings: true, error: null });
    try {
      const res = await mainApi.get(`feed_explore/${type}_best?key=${nextData}`);
      console.log("plplplpl", type, res.data);
      set((state) => ({
        feedDatas: [...state.feedDatas, ...res.data.body.send_data],
        nextKey: res.data.body.key,
        loadings: false,
      }));
    } catch (err) {
      set({ error: err.message, loadings: false });
    }
  },

  fetchFeedWithTag: async (type, tag) => {
    set({ loadings: true, error: null, feedDatas: [] });
    try {
      let target_time = "";
      if (type === "today") {
        target_time = "day";
      } else if (type === "weekly") {
        target_time = "weekly";
      }
      console.log(type, tag, target_time);
      const res = await mainApi.get(
        `feed_explore/search_feed_with_hashtag?hashtag=${tag}&key=-1&target_time=${target_time}`
      );
      console.log("clclclcl", res.data);
      set({
        feedDatas: res.data.body.send_data,
        loadings: false,
      });
    } catch (err) {
      set({ error: err.message, loadings: false });
    }
  },
}));

export default useFeedStore;
