#!/usr/bin/env python3
"""Navigation Le Fil dans l'accueil connecte, branchee sur Element X natif."""
from pathlib import Path
p=Path("upstream/features/home/impl/src/main/kotlin/io/element/android/features/home/impl/HomeView.kt")
s=p.read_text()
anchor="import androidx.compose.foundation.layout.Box\n"
assert s.count(anchor)==1
s=s.replace(anchor,anchor+"""import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
""")
anchor="import io.element.android.libraries.designsystem.theme.components.Scaffold\n"
assert s.count(anchor)==1
s=s.replace(anchor,anchor+"""import io.element.android.libraries.designsystem.theme.components.Text
import io.element.android.libraries.designsystem.theme.components.Button
""")
anchor="                when (state.currentHomeNavigationBarItem) {\n                    HomeNavigationBarItem.Chats -> {\n                        RoomListContentView("
assert s.count(anchor)==1
s=s.replace(anchor,"""                Column {
                    LeFilNavigation(
                        onPapoteClick = {
                            leFilSpaceSection = null
                            state.eventSink(HomeEvent.SelectHomeNavigationBarItem(HomeNavigationBarItem.Chats))
                            onStartChatClick()
                        },
                        onSentiersClick = {
                            leFilSpaceSection = "Sentiers"
                            state.eventSink(HomeEvent.SelectHomeNavigationBarItem(HomeNavigationBarItem.Spaces))
                        },
                        onOasisClick = {
                            leFilSpaceSection = "Oasis"
                            state.eventSink(HomeEvent.SelectHomeNavigationBarItem(HomeNavigationBarItem.Spaces))
                        },
                    )
                    Box(modifier = Modifier.weight(1f)) {
                when (state.currentHomeNavigationBarItem) {
                    HomeNavigationBarItem.Chats -> {
                        RoomListContentView(""")
anchor="""                }
            }
        },
        snackbarHost = { SnackbarHost(snackbarHostState) },"""
assert s.count(anchor)==1
s=s.replace(anchor,"""                }
                    }
                }
            }
        },
        snackbarHost = { SnackbarHost(snackbarHostState) },""")
anchor="@Composable\nprivate fun HomeFloatingActionButton("
assert s.count(anchor)==1
s=s.replace(anchor,"""/**
 * Acces directs aux fonctions existantes : aucune creation de salon implicite.
 * Papote ouvre le parcours natif de demarrage d'une conversation.
 * Sentiers et Oasis ouvrent les espaces Matrix existants du compte.
 */
@Composable
private fun LeFilNavigation(
    onPapoteClick: () -> Unit,
    onSentiersClick: () -> Unit,
    onOasisClick: () -> Unit,
) {
    Column(modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp)) {
        Text(
            text = "Le Fil",
            style = ElementTheme.typography.fontHeadingMdBold,
            color = ElementTheme.colors.textPrimary,
        )
        Text(
            text = "Se relier malgré la distance et la dispersion",
            style = ElementTheme.typography.fontBodySmRegular,
            color = ElementTheme.colors.textSecondary,
        )
        Spacer(modifier = Modifier.height(8.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Button(text = "Papote", onClick = onPapoteClick, modifier = Modifier.weight(1f))
            Button(text = "Sentiers", onClick = onSentiersClick, modifier = Modifier.weight(1f))
            Button(text = "Oasis", onClick = onOasisClick, modifier = Modifier.weight(1f))
        }
    }
}

@Composable
private fun HomeFloatingActionButton(""")
assert s.count('private fun LeFilNavigation(') == 1
assert s.count('RoomListContentView(') >= 1
assert s.count('HomeSpacesView(') >= 1
assert s.count('onRoomClick(spaceId)') == 1
# Le filtre est facultatif : l'onglet natif Espaces conserve la liste complete.
space_path = Path("upstream/features/home/impl/src/main/kotlin/io/element/android/features/home/impl/spaces/HomeSpacesView.kt")
space_src = space_path.read_text()
old = """    state: HomeSpacesState,
    lazyListState: LazyListState,"""
assert space_src.count(old) == 1
space_src = space_src.replace(old, """    state: HomeSpacesState,
    leFilSection: String? = null,
    lazyListState: LazyListState,""")
old = "    if (state.spaceRooms.isEmpty()) {"
assert space_src.count(old) == 1
space_src = space_src.replace(old, """    val visibleSpaces = if (leFilSection == null) {
        state.spaceRooms
    } else {
        state.spaceRooms.filter { space ->
            val name = space.displayName.trim()
            name.equals(leFilSection, ignoreCase = true) ||
                name.startsWith("$leFilSection ·", ignoreCase = true) ||
                name.startsWith("$leFilSection -", ignoreCase = true) ||
                name.startsWith("$leFilSection /", ignoreCase = true)
        }
    }
    if (visibleSpaces.isEmpty()) {""")
assert space_src.count("items = state.spaceRooms,") == 1
space_src = space_src.replace("items = state.spaceRooms,", "items = visibleSpaces,")
space_src = space_src.replace("numberOfSpaces = state.spaceRooms.size", "numberOfSpaces = visibleSpaces.size")
space_src = space_src.replace("index != state.spaceRooms.lastIndex", "index != visibleSpaces.lastIndex")
space_path.write_text(space_src)
p.write_text(s)
print("Navigation Le Fil connectee aux ecrans natifs Chats / Spaces / StartChat.")
