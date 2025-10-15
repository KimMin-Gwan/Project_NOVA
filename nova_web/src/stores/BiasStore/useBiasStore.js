import { create } from "zustand";
import getBiasList from "../../services/getBiasList";
const useBiasStore = create((set) => (
  {
  biasList: [],
  loading: false,
  error: null,
  biasId: "",

  setBiasId: (bid) => set({ biasId: bid }),

  fetchBiasList: async () => {
    set({ loading: true, error: null });
    try {
      const res = await getBiasList();
      set({ biasList: res.body.bias_list, loading: false });
    } catch (err) {
      set({ error: err.message, loading: false });
    }
  },
}));

export default useBiasStore;
