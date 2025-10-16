import { createRouter, createWebHistory } from 'vue-router'
// import HomeView from '../views/HomeView.vue'
import HomeView from '@/components/HomeView.vue';
import AdminLogin from '@/components/AdminLogin.vue';
import UserLogin from '@/components/UserLogin.vue';
import AdminDashboard from '@/components/AdminDashboard.vue';
import UserDashboard from '@/components/UserDashboard.vue';
import UserSignup from '@/components/UserSignup.vue';
import SubjectView from '@/components/SubjectView.vue';
import ChapterView from '@/components/ChapterView.vue';
import QuizView from '@/components/QuizView.vue';
import QuestionView from '@/components/QuestionView.vue';
import UserView from '@/components/UserView.vue';
import AddSubject from '@/components/AddSubject.vue';
import AddChapter from '@/components/AddChapter.vue';
import AddQuiz from '@/components/AddQuiz.vue';
import AddQuestion from '@/components/AddQuestion.vue';
import ExamView from '@/components/ExamView.vue';
import ResultView from '@/components/ResultView.vue';
import SummaryUser from '@/components/SummaryUser.vue';
import EditSubject from '@/components/EditSubject.vue';
import EditChapter from '@/components/EditChapter.vue';
import EditQuiz from '@/components/EditQuiz.vue';
import EditQuestion from '@/components/EditQuestion.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/admin-login',
      name: 'admin-login',
      component: AdminLogin,
    },
    {
      path: '/student-login',
      name: 'student-login',
      component: UserLogin,
    },
    {
      path: '/admin-dashboard',
      name: 'admin',
      component: AdminDashboard,
    },
    {
      path: '/student-dashboard',
      name: 'student',
      component: UserDashboard,
    },
    {
      path: '/signup',
      name: 'signup',
      component: UserSignup,
    },
    {
      path: '/admin-subjects',
      name: 'admin-subjects',
      component: SubjectView,
    },
    {
      path: '/chapters',
      name: 'chapters',
      component: ChapterView,
    },
    {
      path: '/quizzes',
      name: 'quizzes',
      component: QuizView,
    },
    {
      path: '/questions',
      name: 'questions',
      component: QuestionView,
    },
    {
      path: '/users',
      name: 'users',
      component: UserView,
    },
    {
      path: '/add-subject',
      name: 'add-subject',
      component: AddSubject,
    },
    {
      path: '/add-chapter',
      name: 'add-chapter',
      component: AddChapter,
    },
    {
      path: '/add-quiz',
      name: 'add-quiz',
      component: AddQuiz,
    },
    {
      path: '/add-question',
      name: 'add-question',
      component: AddQuestion,
    },
    {
      path: '/exam/:id',
      name: 'exam',
      component: ExamView,
    },
    {
      path: '/result/:id',
      name: 'result',
      component: ResultView,
    },
    {
      path: '/user_summary',
      name: 'summary',
      component: SummaryUser,
    },
    {
      path: '/edit-subject/:id',
      name: 'edit-subject',
      component: EditSubject,
    },
    {
      path: '/edit-chapter/:id',
      name: 'edit-chapter',
      component: EditChapter,
    },
    {
      path: '/edit-quiz/:id',
      name: 'edit-quiz',
      component: EditQuiz,
    },
    {
      path: '/edit-question/:id',
      name: 'edit-question',
      component: EditQuestion,
    },
  ],
})

export default router
