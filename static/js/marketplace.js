/************************** MARKETPLACE **************************/

import { MDCDrawer } from "@material/drawer";
import { MDCTopAppBar } from '@material/top-app-bar';


/************************** FUNCTIONS **************************/

// Top App Bar, Drawer and Main Content
const drawerEl = document.querySelector('.container-marketplace--drawer');
const drawer = MDCDrawer.attachTo(drawerEl);
const mainContentEl = document.querySelector('.container-marketplace--main-content');
const topAppBarEl = document.querySelector('.container-marketplace--topappbar');
const topAppBar = new MDCTopAppBar(topAppBarEl);
topAppBar.setScrollTarget(mainContentEl);
topAppBar.listen('MDCTopAppBar:nav', () => {
    drawer.open = !drawer.open;
});
