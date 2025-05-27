import { createRouter, createWebHistory } from 'vue-router';
import AnnouncementPage from './components/Announcement.vue'; // 新增公告頁面
import AnnouncementList from './components/AnnouncementList.vue'; // 顯示所有公告的頁面

const routes = [
    {
        path: '/',
        name: 'AnnouncementList',
        component: AnnouncementList
    },
    {
        path: '/add-announcement',
        name: 'AddAnnouncement',
        component: AnnouncementPage
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;