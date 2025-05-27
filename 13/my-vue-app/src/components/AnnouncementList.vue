<template>
  <div>
    <h1>所有公告</h1>
    <router-link to="/add-announcement">新增公告</router-link>
    <table>
      <thead>
        <tr>
          <th>編號</th>
          <th>公告內容</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="announcement in announcements" :key="announcement.id">
          <td>{{ announcement.id }}</td>
          <td>{{ announcement.text }}</td>
          <td>
            <button @click="editAnnouncement(announcement.id)">編輯</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      announcements: []
    };
  },
  methods: {
    fetchAnnouncements() {
      fetch('http://localhost:5000/announcements')
        .then(response => response.json())
        .then(data => {
          this.announcements = data;
        });
    }
  },
  mounted() {
    this.fetchAnnouncements();
  }
};
</script>

<style>
/* 您的樣式 */
</style>
