<template>
  <div>
    <div class="container">
      <b-button @click="fetchActivity">Fetch recent activity</b-button>
    </div>
        <b-table
            :data="games"
            detailed
            @details-open="(row) => this.getDetails(row)"
            :paginated="isPaginated"
            :per-page="perPage"
            :current-page.sync="currentPage"
            :loading="tableLoading"
            default-sort="row.game"
            aria-next-label="Next page"
            aria-previous-label="Previous page"
            aria-page-label="Page"
            aria-current-label="Current page">

            <template slot-scope="props">
                <b-table-column field="date" label="date" width="40" sortable>
                  {{ props.row.date }}
                </b-table-column>
                <b-table-column field="name" label="Game"  sortable>
                  {{ props.row.name }}
                </b-table-column>
                <b-table-column field="type" label="type" sortable>
                  {{ props.row.type }}
                </b-table-column>
            </template>

          <template slot="detail" slot-scope="props">
                <article class="media">
                    <div class="media-content" v-if="details[`${props.row.href}`]">
                      <h1>{{ details[props.row.href].header }}</h1>
                      <p>{{ details[props.row.href].publish_date }}</p>

                      <ul>
                        <li v-for="(tag, index) in details[`${props.row.href}`].tags"
                            :key="index">
                          <a :href="tag.href">
                            {{ tag.name }}
                          </a>
                        </li>
                      </ul>

                      <div>
                        <img :src="img"
                             alt=""
                             v-for="(img, index) in details[`${props.row.href}`].images"
                            :key="index">
                      </div>

                      <ul>
                        <li v-for="(download,index) in details[`${props.row.href}`].downloads"
                        :key="index">
                          <a :href="download">{{ download }}</a>
                        </li>
                      </ul>

                      <div>
                      <div v-for="(release, index) in details[`${props.row.href}`].updates"
                           :key="index">
                        <h3>{{ release.version }}</h3>
                          <ul>
                            <li v-for="(update, index) in release.links" :key="index">
                              <a :href="update">{{update}}</a>
                            </li>
                          </ul>
                      </div>
                      </div>
<!--                      <p>{{ details[props.row.href].description }}</p>-->

                    </div>
                </article>
            </template>
        </b-table>
    </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';

export default {
  name: 'TableRecentActivity',
  data() {
    return {
      loading: false,
      isPaginated: true,
      isPaginationSimple: false,
      paginationPosition: 'bottom',
      defaultSortDirection: 'asc',
      sortIcon: 'arrow-up',
      sortIconSize: 'is-small',
      currentPage: 1,
      perPage: 25,
    };
  },
  computed: mapState({
    games: state => state.recentActivity,
    details: state => state.gameDetails,
    tableLoading: state => state.RecentActivityLoading,
  }),
  methods: {
    ...mapActions({
      fetchActivity: 'fetchActivity',
      getDetails: 'getDetails',
    }),
  },
};
</script>

<style scoped>

</style>
