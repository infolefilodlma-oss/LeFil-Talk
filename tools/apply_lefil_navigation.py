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
                            state.eventSink(HomeEvent.SelectHomeNavigationBarItem(HomeNavigationBarItem.Chats))
                            onStartChatClick()
                        },
                        onSentiersClick = {
                            state.eventSink(HomeEvent.SelectHomeNavigationBarItem(HomeNavigationBarItem.Spaces))
                        },
                        onOasisClick = {
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
p.write_text(s)
print("Navigation Le Fil connectee aux ecrans natifs Chats / Spaces / StartChat.")
