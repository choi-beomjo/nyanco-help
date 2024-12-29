<template>
    <div>
      <h1>Properties List</h1>
      <div v-if="properties.length">
        <ul>
          <PropertyItem
            v-for="property in properties"
            :key="property.id"
            :property="property"
            @edit="goToEdit"
          />
        </ul>
      </div>
      <div v-else>
        <p>No properties found.</p>
      </div>
      <BackButton />
    </div>
  </template>
  
  <script>
  import axios from "@/services/axios.js"; // Axios로 API 호출
  import PropertyItem from "@/components/property/PropertyItem.vue";
  import BackButton from "@/components/common/BackButton.vue";

  export default {
    components:{
      PropertyItem,
      BackButton,
    },
    data() {
      return {
        properties: [], // 적 데이터 저장
      };
    },
    created() {
      this.fetchProperties(); // 페이지 생성 시 API 호출
    },
    methods: {
      async fetchProperties() {
        try {
          const response = await axios.get("/api/property/list");
          this.properties = response.data; // API 응답 저장
        } catch (error) {
          console.error("Error fetching properties:", error);
        }
      },
      goBack() {
        this.$router.push("/"); // 홈으로 이동
      },
      goToEdit(propertyId) {
        this.$router.push(`/property/edit/${propertyId}`);
      },
    },
  };
  </script>
  