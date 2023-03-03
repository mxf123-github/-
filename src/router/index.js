import Manage_page from '../views/Manage_page.vue'
import Payment_page from '../views/Payment_page.vue'

const routes = [
  {
    path: '/',
    name: 'Manage_page',
    component: Manage_page,
  },
  {
    path: '/Payment_page',
    name: 'Payment_page',
    component: Payment_page,
  },
]

export default routes
