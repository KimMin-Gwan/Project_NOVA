// import { create } from "zustand";
// import mainApi from "../../services/apis/mainApi";
// import postApi from "../../services/apis/postApi";
// import HEADER from "../../constant/header";

// const useFeedStore = create((set, get) => ({
//   feedDatas: [],
//   nextKey: -1,
//   loadings: false,
//   hasMore: true,
//   error: null,
//   activeTag: null,
//   isTagSwitching: false,

//   fetchAllFeedList: async (type, clickedFetch) => {
//     let updatedNextData = -1;

//     //  만약 적용 버튼을 누르면 -1로 세팅
//     if (clickedFetch) {
//       updatedNextData = -1;
//       set({ nextKey: -1 });
//     }
//     // 그게 아닌 상황에서는 기존의 nextData 를 사용
//     else {
//       updatedNextData = get().nextKey;
//     }

//     set({ loadings: true, error: null, feedDatas: [] });

//     try {
//       const res = await postApi.post(`feed_explore/all_feed`, {
//         header: HEADER,
//         body: {
//           key: updatedNextData, // 여기에서  사용됨
//           category: filterCategory || [""],
//           fclass: filterFclass || "",
//         },
//       });
//       set({
//         feedDatas: res.data.body.send_data,
//         nextKey: res.data.body.key,
//         loadings: false,
//       });
//     } catch (err) {
//       set({ err: err.message, loadings: false });
//     }
//   },

//   fetchFeedList: async (type) => {
//     set({ loadings: true, error: null, feedDatas: [] });
//     try {
//       const res = await mainApi.get(`feed_explore/${type}_best`);
//       console.log("rererere", type, res.data);
//       set({ feedDatas: res.data.body.send_data, nextKey: res.data.body.key, loadings: false });
//     } catch (err) {
//       set({ error: err.message, loadings: false });
//     }
//   },

//   fetchMoreFeedList: async (type, nextData) => {
//     const { nextKey, hasMore, loadings, isTagSwitching } = get();
//     if (!hasMore || loadings || isTagSwitching) return;

//     set({ loadings: true, error: null });
//     try {
//       const res = await mainApi.get(`feed_explore/${type}_best?key=${nextKey}`);
//       console.log("plplplpl", type, res.data);
//       set((state) => ({
//         feedDatas: [...state.feedDatas, ...res.data.body.send_data],
//         nextKey: res.data.body.key,
//         loadings: false,
//         hasMore: res.data.body.send_data.length > 0,
//       }));
//     } catch (err) {
//       set({ error: err.message, loadings: false });
//     }
//   },

//   fetchFeedWithTag: async (type, tag) => {
//     set({ loadings: true, error: null, feedDatas: [], isTagSwitching: true });
//     try {
//       let target_time = "";
//       if (type === "today") {
//         target_time = "day";
//       } else if (type === "weekly") {
//         target_time = "weekly";
//       } else return;
//       console.log(type, tag, target_time);
//       const res = await mainApi.get(
//         `feed_explore/search_feed_with_hashtag?hashtag=${tag}&key=-1&target_time=${target_time}`
//       );
//       console.log("clclclcl", res.data);
//       set({
//         feedDatas: res.data.body.send_data,
//         loadings: false,
//         isTagSwitching: false,
//       });
//     } catch (err) {
//       set({ error: err.message, loadings: false });
//     }
//   },

//   resetFeedList: () => {
//     set({
//       feedDatas: [],
//       nextKye: -1,
//       loadings: false,
//       error: null,
//       hasMore: true,
//       isTagSwitching: false,
//     });
//   },
// }));

// export default useFeedStore;
