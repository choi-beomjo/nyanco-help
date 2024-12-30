import PropertyListView from '@/views/property/PropertyListView.vue';
import AddProperty from '@/views/property/AddProperty.vue';

export default [
    { path: "/property-list", name: "PropertyList", component: PropertyListView },
    { path: "/property/add", component: AddProperty},
]