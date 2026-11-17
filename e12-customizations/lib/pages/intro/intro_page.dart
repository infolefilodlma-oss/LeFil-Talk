// SPDX-FileCopyrightText: 2019-Present Christian Kußowski
// SPDX-FileCopyrightText: 2019-Present Contributors to FluffyChat
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import 'package:flutter/gestures.dart';
import 'package:fluffychat/config/setting_keys.dart';
import 'package:fluffychat/l10n/l10n.dart';
import 'package:fluffychat/pages/intro/flows/restore_backup_flow.dart';
import 'package:fluffychat/utils/platform_infos.dart';
import 'package:fluffychat/widgets/layouts/login_scaffold.dart';
import 'package:fluffychat/widgets/matrix.dart';
import 'package:go_router/go_router.dart';
import 'package:material_ui/material_ui.dart';
import 'package:url_launcher/url_launcher_string.dart';

class IntroPage extends StatelessWidget {
  final bool isLoading, hasPresetHomeserver;
  final String? loggingInToHomeserver, welcomeText;
  final VoidCallback login;

  const IntroPage({
    required this.isLoading,
    required this.loggingInToHomeserver,
    super.key,
    required this.hasPresetHomeserver,
    required this.welcomeText,
    required this.login,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final addMultiAccount = Matrix.of(
      context,
    ).widget.clients.any((client) => client.isLogged());
    final loggingInToHomeserver = this.loggingInToHomeserver;

    return LoginScaffold(
      appBar: AppBar(
        centerTitle: true,
        title: addMultiAccount
            ? Text(L10n.of(context).addAccount)
            : Text(AppSettings.applicationName.value),
        actions: [
          PopupMenuButton(
            useRootNavigator: true,
            itemBuilder: (_) => [
              PopupMenuItem(
                onTap: isLoading ? null : () => restoreBackupFlow(context),
                child: Row(
                  mainAxisSize: .min,
                  spacing: 12,
                  children: [
                    const Icon(Icons.import_export_outlined),
                    Expanded(
                      child: Text(
                        L10n.of(context).hydrate,
                        maxLines: 1,
                        overflow: .ellipsis,
                      ),
                    ),
                  ],
                ),
              ),
              PopupMenuItem(
                onTap: () => launchUrlString(AppSettings.privacyPolicy.value),
                child: Row(
                  mainAxisSize: .min,
                  spacing: 12,
                  children: [
                    const Icon(Icons.privacy_tip_outlined),
                    Text(L10n.of(context).privacy),
                  ],
                ),
              ),
              PopupMenuItem(
                onTap: () => PlatformInfos.showDialog(context),
                child: Row(
                  mainAxisSize: .min,
                  spacing: 12,
                  children: [
                    const Icon(Icons.info_outlined),
                    Text(L10n.of(context).about),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),
      body: isLoading
          ? Center(
              child: Column(
                mainAxisAlignment: .center,
                children: [
                  CircularProgressIndicator.adaptive(),
                  if (loggingInToHomeserver != null)
                    Text(L10n.of(context).logInTo(loggingInToHomeserver)),
                ],
              ),
            )
          : LayoutBuilder(
              builder: (context, constraints) {
                return SingleChildScrollView(
                  child: ConstrainedBox(
                    constraints: BoxConstraints(
                      minHeight: constraints.maxHeight,
                    ),
                    child: IntrinsicHeight(
                      child: Column(
                        children: [
                          Container(
                            alignment: Alignment.center,
                            padding: const EdgeInsets.all(32.0),
                            child: Hero(
                              tag: 'info-logo',
                              child: ClipRRect(
                                borderRadius: BorderRadius.circular(128),
                                child: Image.asset(
                                  './assets/logo/mini/le_fil_echo_logo.jpg',
                                  width: 128,
                                  height: 128,
                                ),
                              ),
                            ),
                          ),
                          Padding(
                            padding: const EdgeInsets.symmetric(horizontal: 24),
                            child: RichText(
                              textAlign: TextAlign.center,
                              text: TextSpan(
                                style: Theme.of(context).textTheme.bodyMedium,
                                children: [
                                  const TextSpan(
                                    text: 'Comme le suggère ',
                                  ),
                                  TextSpan(
                                    text: 'Le Signe',
                                    style: TextStyle(
                                      color: theme.colorScheme.primary,
                                      decoration: TextDecoration.underline,
                                    ),
                                    recognizer: TapGestureRecognizer()
                                      ..onTap = () => launchUrlString(
                                        'https://le-fil.net/lesigne.html',
                                      ),
                                  ),
                                  const TextSpan(
                                    text: ', la foi ne s\'arrête pas à celui qui la reçoit : elle trouve un écho dans ceux qui la vivent et la transmettent.',
                                  ),
                                ],
                              ),
                            ),
                          ),
                          const SizedBox(height: 20),
                          Text(
                            'Pourquoi Le Fil a-t-il choisi Matrix ?',
                            textAlign: TextAlign.center,
                            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                          ),
                          const SizedBox(height: 8),
                          Padding(
                            padding: const EdgeInsets.symmetric(horizontal: 24),
                            child: RichText(
                              textAlign: TextAlign.center,
                              text: TextSpan(
                                style: Theme.of(context).textTheme.bodyMedium,
                                children: [
                                  const TextSpan(
                                    text: 'Le Fil a choisi ',
                                  ),
                                  TextSpan(
                                    text: 'Matrix',
                                    style: TextStyle(
                                      color: theme.colorScheme.primary,
                                      decoration: TextDecoration.underline,
                                    ),
                                    recognizer: TapGestureRecognizer()
                                      ..onTap = () => launchUrlString(
                                        'https://matrix.org/fr/',
                                      ),
                                  ),
                                  const TextSpan(
                                    text: ' pour sa messagerie Écho parce que ce réseau ouvert, soutenu par une fondation à but non lucratif, partage nos valeurs : la liberté de communiquer, le respect de la vie privée, l\'indépendance et le refus de l\'exploitation commerciale de nos échanges.',
                                  ),
                                ],
                              ),
                            ),
                          ),
                          const Spacer(),
                          Padding(
                            padding: const EdgeInsets.symmetric(horizontal: 32),
                            child: Column(
                              mainAxisSize: .min,
                              crossAxisAlignment: .stretch,
                              children: [
                                if (!hasPresetHomeserver)
                                  ElevatedButton(
                                    style: ElevatedButton.styleFrom(
                                      backgroundColor:
                                          theme.colorScheme.secondary,
                                      foregroundColor:
                                          theme.colorScheme.onSecondary,
                                    ),
                                    onPressed: () => context.go(
                                      '${GoRouterState.of(context).uri.path}/sign_up',
                                    ),
                                    child: Text(
                                      L10n.of(context).createNewAccount,
                                    ),
                                  ),
                                SizedBox(height: 16),
                                ElevatedButton(
                                  onPressed: login,
                                  child: Text(L10n.of(context).signIn),
                                ),

                                if (!hasPresetHomeserver)
                                  TextButton(
                                    onPressed: () async {
                                      final client = await Matrix.of(
                                        context,
                                      ).getLoginClient();
                                      if (!context.mounted) return;
                                      context.go(
                                        '${GoRouterState.of(context).uri.path}/login',
                                        extra: client,
                                      );
                                    },
                                    child: Text(
                                      L10n.of(context).loginWithMatrixId,
                                    ),
                                  ),
                              ],
                            ),
                          ),
                          const SizedBox(height: 36),
                        ],
                      ),
                    ),
                  ),
                );
              },
            ),
    );
  }
}
