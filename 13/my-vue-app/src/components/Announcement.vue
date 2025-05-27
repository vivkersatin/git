<template>
  <div>
    <h1>公告系統</h1>
    <form @submit.prevent="addAnnouncement">
      <input v-model="newAnnouncement" placeholder="輸入公告" />
      <button type="submit">新增公告</button>
    </form>
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
          <td class="center">{{ announcement.id }}</td>
          <td>{{ announcement.text }}</td>
          <td class="center">
            <button @click="editAnnouncement(announcement.id)">編輯</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-if="editingIndex !== null">
      <input v-model="editedAnnouncement" placeholder="編輯公告" />
      <button @click="updateAnnouncement">更新公告</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AnnouncementComponent',
  data() {
    return {
      announcements: [],
      newAnnouncement: '',
      editingIndex: null,
      editedAnnouncement: ''
    };
  },
  methods: {
    fetchAnnouncements() {
      fetch('http://localhost:5000/announcements')
        .then(response => response.json())
        .then(data => {
          this.announcements = data;
        });
    },
    addAnnouncement() {
      const announcement = { text: this.newAnnouncement };
      fetch('http://localhost:5000/announcements', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(announcement)
      })
      .then(response => response.json())
      .then(data => {
        this.announcements.push(data);
        this.newAnnouncement = '';
      });
    },
    editAnnouncement(id) {
      this.editingIndex = id; // 使用公告的 ID
      this.editedAnnouncement = this.announcements.find(a => a.id === id).text;
    },
    updateAnnouncement() {
      const announcement = { text: this.editedAnnouncement };
      fetch(`http://localhost:5000/announcements/${this.editingIndex}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(announcement)
      })
      .then(response => response.json())
      .then(data => {
        const index = this.announcements.findIndex(a => a.id === this.editingIndex);
        this.announcements[index] = data; // 更新公告
        this.editingIndex = null;
        this.editedAnnouncement = '';
      });
    }
  },
  mounted() {
    this.fetchAnnouncements();
  }
};
</script>

<style>
table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center; /* 置中顯示 */
}
th {
  background-color: #f2f2f2;
}
</style>