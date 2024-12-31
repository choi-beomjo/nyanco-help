import SkillListView from "@/views/skill/SkillListView.vue";
import AddSkill from "@/views/skill/AddSkill.vue";

export default [
    { path: "/skill-list", name: "SkillList", component: SkillListView },
    { path: "/skill/add", component: AddSkill},
];