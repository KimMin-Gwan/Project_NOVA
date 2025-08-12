    def set_best_feed_with_time(self, feed_search_engine:FeedSearchEngine, feed_manager:FeedManager,
                                search_type, time_type, last_index=-1, num_feed=4):
        
        fid_list = feed_search_engine.try_get_feed_in_recent(search_type=search_type, time_type=time_type)
        fid_list, self._key = feed_manager.paging_fid_list(fid_list, last_index=last_index, page_size=num_feed)
        self._send_data = self._make_feed_data_n_interaction_data(feed_manager=feed_manager, fid_list=fid_list)
        return