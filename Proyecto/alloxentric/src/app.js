import axios from 'axios';
import config from "@/config";

export default {
  data() {
    return {
      plans: [],
    };
  },
  methods: {
    async fetchPlans() {
      try {
        const response = await axios.get(`${config.BASE_URL}:8000/plans`);
        this.plans = response.data;
      } catch (error) {
        console.error("Error fetching plans:", error);
      }
    },
  },
  mounted() {
    this.fetchPlans();
  },
};

