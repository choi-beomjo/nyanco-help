import CharacterListView from "@/views/character/CharacterListView.vue";
import CharacterEdit from '@/views/character/CharacterEdit.vue';
import AddCharacter from '@/views/character/AddCharacter.vue';
import CharacterSearch from "@/views/character/CharacterSearch.vue";


export default [
  { path: "/character-list", name: "CharacterList", component: CharacterListView },
  { path: "/character/edit/:id", component: CharacterEdit, props: true },
  { path: "/character/add", component: AddCharacter},
  { path: "/character/search", component: CharacterSearch},
];